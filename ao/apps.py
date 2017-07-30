"""Apps for ao"""
from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class AoConfig(AppConfig):
    """
    Config for ao application.
    """
    name = 'ao'
    label = 'ao'
    verbose_name = _('ao')

    # def ready(self):
    #     from . import checks
