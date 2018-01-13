from django.conf.urls import include, url
from django.contrib import admin
from ao.tests.testproject import views

urlpatterns = [
    # url(r'^(?P<url>.*)$', views.debug, name="debug"),
    url(r'^', include('ao.msazure.urls')),
    url(r'^http://api.upcloud.com/1.2/', include('ao.upcloud.urls')),
    url('admin/', admin.site.urls),
]
