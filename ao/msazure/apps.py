"""Apps for ao.msazure"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MsAzureConfig(AppConfig):
    """
    Config for ao application.
    """
    name = 'msazure'
    label = 'msazure'
    verbose_name = _('Microsoft Azure')

    # def ready(self):
    #     from . import checks
