from django.conf import settings
from ao import settings as ao_settings

MODE = getattr(settings, 'AO_MSAZURE_MODE', ao_settings.MODE)
