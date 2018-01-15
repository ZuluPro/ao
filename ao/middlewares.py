import re
from urllib.parse import urlparse
from django.core import handlers
from django.urls.exceptions import Resolver404


class ProxyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'CONNECT':
            from django.http import HttpResponse
            return HttpResponse()
        resolver = handlers.base.get_resolver('ao.cloud_urls')
        old_resolver_regex = resolver.regex
        resolver.regex = re.compile('^')
        try:
            cloud_urls = resolver.resolve(request.path_info).func()
            cloud_resolver = handlers.base.get_resolver(cloud_urls)
        except Resolver404 as err:
            # Normal behavior
            url = urlparse(request.path_info)
            resolver.regex = old_resolver_regex
            request.path = request.path_info = url.path
            return self.get_response(request)
        url = urlparse(request.path_info)
        resolved = cloud_resolver.resolve(url.path)
        return resolved.func(request, *resolved.args, **resolved.kwargs)
