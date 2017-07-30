from django.conf import settings

MODE = getattr(settings, 'AO_MODE', 'cool')
