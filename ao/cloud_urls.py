from django.conf.urls import include, url


urlpatterns = [
    url(r'^https?://api.upcloud.com(:80|:443)?/', lambda: 'ao.upcloud.urls'),
]
