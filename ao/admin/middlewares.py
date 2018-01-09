from django.contrib.auth.middleware import AuthenticationMiddleware


class AdminAuthenticationMiddleware(AuthenticationMiddleware):
    def process_request(self, request):
        if request.path.startswith('/admin/'):
            super(AdminAuthenticationMiddleware, self).process_request(request)
