import sys
import os
import threading
import socket
import ssl
import time
import select
from subprocess import Popen, PIPE
try:
    from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
    from SocketServer import ThreadingMixIn
except ImportError:
    from http.server import BaseHTTPRequestHandler, HTTPServer
    from socketserver import ThreadingMixIn

from django.core.management.base import BaseCommand, CommandError


def join_with_script_dir(path):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), path)


class ThreadingHTTPServer(ThreadingMixIn, HTTPServer):
    address_family = socket.AF_INET6
    daemon_threads = True

    def handle_error(self, request, client_address):
        # surpress socket/ssl related errors
        cls, e = sys.exc_info()[:2]
        if cls is socket.error or cls is ssl.SSLError:
            pass
        else:
            return HTTPServer.handle_error(self, request, client_address)


class ProxyRequestHandler(BaseHTTPRequestHandler):
    cakey = join_with_script_dir('ca.key')
    cacert = join_with_script_dir('ca.crt')
    certkey = join_with_script_dir('cert.key')
    certdir = join_with_script_dir('certs/')
    timeout = 5
    lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        self.tls = threading.local()
        self.tls.conns = {}
        BaseHTTPRequestHandler.__init__(self, *args, **kwargs)

    def log_error(self, format, *args):
        # surpress "Request timed out: timeout('timed out',)"
        if isinstance(args[0], socket.timeout):
            return

        self.log_message(format, *args)

    def do_CONNECT(self):
        if os.path.isfile(self.cakey) and os.path.isfile(self.cacert) and os.path.isfile(self.certkey) and os.path.isdir(self.certdir):
            self.connect_intercept()
        else:
            self.connect_relay()

    def connect_intercept(self):
        hostname = self.path.split(':')[0]
        certpath = "%s/%s.crt" % (self.certdir.rstrip('/'), hostname)

        with self.lock:
            if not os.path.isfile(certpath):
                epoch = "%d" % (time.time() * 1000)
                p1 = Popen(["openssl", "req", "-new", "-key", self.certkey, "-subj", "/CN=%s" % hostname], stdout=PIPE)
                p2 = Popen(["openssl", "x509", "-req", "-days", "3650", "-CA", self.cacert, "-CAkey", self.cakey, "-set_serial", epoch, "-out", certpath], stdin=p1.stdout, stderr=PIPE)
                p2.communicate()

        self.wfile.write("%s %d %s\r\n" % (self.protocol_version, 200, 'Connection Established'))
        self.end_headers()

        self.connection = ssl.wrap_socket(self.connection, keyfile=self.certkey, certfile=certpath, server_side=True)
        self.rfile = self.connection.makefile("rb", self.rbufsize)
        self.wfile = self.connection.makefile("wb", self.wbufsize)

        conntype = self.headers.get('Proxy-Connection', '')
        if self.protocol_version == "HTTP/1.1" and conntype.lower() != 'close':
            self.close_connection = 0
        else:
            self.close_connection = 1

    def connect_relay(self):
        address = self.path.split(':', 1)
        address[1] = int(address[1]) or 443
        try:
            s = socket.create_connection(('localhost', 8001), timeout=self.timeout)
        except Exception as e:
            self.send_error(502)
            return
        self.send_response(200, 'Connection Established')
        self.end_headers()

        conns = [self.connection, s]
        self.close_connection = 0
        while not self.close_connection:
            rlist, wlist, xlist = select.select(conns, [], conns, self.timeout)
            if xlist or not rlist:
                break
            for r in rlist:
                other = conns[1] if r is conns[0] else conns[0]
                data = r.recv(8192)
                if not data:
                    self.close_connection = 1
                    break
                other.sendall(data)

    def do_GET(self):
        if self.path == 'http://proxy2.test/':
            self.send_cacert()
            return

        req = self
        content_length = int(req.headers.get('Content-Length', 0))
        req_body = self.rfile.read(content_length) if content_length else None

        if req.path[0] == '/':
            if isinstance(self.connection, ssl.SSLSocket):
                req.path = "https://%s%s" % (req.headers['Host'], req.path)
            else:
                req.path = "http://%s%s" % (req.headers['Host'], req.path)

        req_body_modified = self.request_handler(req, req_body)
        if req_body_modified is False:
            self.send_error(403)
            return
        elif req_body_modified is not None:
            req_body = req_body_modified
            req.headers['Content-length'] = str(len(req_body))

        u = urlparse.urlsplit(req.path)
        scheme, netloc, path = u.scheme, u.netloc, (u.path + '?' + u.query if u.query else u.path)
        assert scheme in ('http', 'https')
        if netloc:
            req.headers['Host'] = netloc
        setattr(req, 'headers', self.filter_headers(req.headers))

        try:
            origin = (scheme, netloc)
            if not origin in self.tls.conns:
                if scheme == 'https':
                    self.tls.conns[origin] = httplib.HTTPSConnection(netloc, timeout=self.timeout)
                else:
                    self.tls.conns[origin] = httplib.HTTPConnection(netloc, timeout=self.timeout)
            conn = self.tls.conns[origin]
            conn.request(self.command, path, req_body, dict(req.headers))
            res = conn.getresponse()

            version_table = {10: 'HTTP/1.0', 11: 'HTTP/1.1'}
            setattr(res, 'headers', res.msg)
            setattr(res, 'response_version', version_table[res.version])

            # support streaming
            if not 'Content-Length' in res.headers and 'no-store' in res.headers.get('Cache-Control', ''):
                self.response_handler(req, req_body, res, '')
                setattr(res, 'headers', self.filter_headers(res.headers))
                self.relay_streaming(res)
                with self.lock:
                    self.save_handler(req, req_body, res, '')
                return

            res_body = res.read()
        except Exception as e:
            if origin in self.tls.conns:
                del self.tls.conns[origin]
            self.send_error(502)
            return

        content_encoding = res.headers.get('Content-Encoding', 'identity')
        res_body_plain = self.decode_content_body(res_body, content_encoding)

        res_body_modified = self.response_handler(req, req_body, res, res_body_plain)
        if res_body_modified is False:
            self.send_error(403)
            return
        elif res_body_modified is not None:
            res_body_plain = res_body_modified
            res_body = self.encode_content_body(res_body_plain, content_encoding)
            res.headers['Content-Length'] = str(len(res_body))

        setattr(res, 'headers', self.filter_headers(res.headers))

        self.wfile.write("%s %d %s\r\n" % (self.protocol_version, res.status, res.reason))
        for line in res.headers.headers:
            self.wfile.write(line)
        self.end_headers()
        self.wfile.write(res_body)
        self.wfile.flush()

        with self.lock:
            self.save_handler(req, req_body, res, res_body_plain)

    def relay_streaming(self, res):
        self.wfile.write("%s %d %s\r\n" % (self.protocol_version, res.status, res.reason))
        for line in res.headers.headers:
            self.wfile.write(line)
        self.end_headers()
        try:
            while True:
                chunk = res.read(8192)
                if not chunk:
                    break
                self.wfile.write(chunk)
            self.wfile.flush()
        except socket.error:
            # connection closed by client
            pass

    do_HEAD = do_GET
    do_POST = do_GET
    do_PUT = do_GET
    do_DELETE = do_GET
    do_OPTIONS = do_GET


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        ProxyRequestHandler.protocol_version = "HTTP/1.1"
        httpd = ThreadingHTTPServer(('::1', 8000), ProxyRequestHandler)
        sa = httpd.socket.getsockname()
        httpd.serve_forever()
