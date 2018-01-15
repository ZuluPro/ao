import requests
import pook
import os 

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ao.tests.testproject.settings")
import django
django.setup()

from . import urls


class Response(object):
    def __init__(self, **kw):
        self._mock = None

    def make_django_request(self, mock):
        if hasattr(self, 'django_response'):
            return
        from ao.tests.testproject.wsgi import application
        # Create Django Request
        request = django.http.request.HttpRequest()
        last_call = mock._calls[-1]
        request.headers = last_call._headers
        request._body = last_call._body
        request.content_type = last_call
        request.path = request.path_info = last_call.url.path
        request.method = last_call._method
        request.META.update(
            CONTENT_LENGTH=len(last_call._body) if last_call._body else 0,
            CONTENT_TYPE=last_call.headers['User-Agent'],
            HTTP_ACCEPT=last_call.headers['Accept'],
            HTTP_ACCEPT_ENCODING=last_call.headers['Accept-Encoding'],
            HTTP_HOST=last_call._url.hostname,
            HTTP_USER_AGENT=last_call.headers['User-Agent'],
            SERVER_NAME=last_call._url.hostname,
            SERVER_PORT=last_call._url.port,
            QUERY_STRING=last_call.url.query,
            REQUEST_METHOD=last_call._method,
        )
        # Get Django Response
        self.django_response = application.get_response(request)
        self.headers = {k: v for t, (k, v) in self.django_response._headers.items()}
        self.body = self.django_response.content if self.django_response.content else b''
        self.__status = self.django_response.status_code

    @property
    def _headers(self):
        if not hasattr(self, 'headers'):
            self.make_django_request(self.mock)
        return self.headers

    @property
    def _body(self):
        if not hasattr(self, 'body'):
            self.make_django_request(self.mock)
        return self.body

    @property
    def _status(self):
        if not hasattr(self, '__status'):
            self.make_django_request(self.mock)
        return self.__status

    def status(self, status):
        if not hasattr(self, '__status') and hasattr(self, 'mock'):
            self.make_django_request(self.mock)
            return self._status
        return None


for path in urls.urlpatterns:
    path = path.regex.pattern
    path = path.replace('^', '')
    url = r'https?://api.upcloud.com(:80|:443)?/' + path
    pook.mock(pook.regex(url), response=Response()).reply()


def mock_upcloud(func):
    def wrapper(*args, **kwargs):
        pook.on()
        func(*args, **kwargs)
        pook.off()
    return wrapper
