import re
from rest_framework import authentication
from rest_framework import exceptions
from . import settings
from . import models
from . import factories

REG_API_KEY = re.compile('^Basic (.*)$')


class UpCloudAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        self.headers = dict([
            (k, request.META[k])
            for k in request.META
            if k.startswith('HTTP_')
        ])
        account = None
        match = REG_API_KEY.match(self.headers.get('HTTP_AUTHORIZATION', ''))
        if 'HTTP_AUTHORIZATION' in self.headers:
            if match is not None:
                api_key = match.groups()[0]
                account = models.Account.objects.filter(api_key=api_key).first()
                if account is not None:
                    return account, None
        if account is None and settings.AUTHENTICATION_LEVEL == 0:
            data = {} if match is None else {'api_key': match.groups()[0]}
            account = factories.AccountFactory(**data)
            return account, None
