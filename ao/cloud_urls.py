from django.conf.urls import include, url


urlpatterns = [
    url(r'^http://api.upcloud.com/1.2/', lambda: 'ao.upcloud.urls'),
]
