from django.conf.urls import include, url
from django.contrib import admin
from ao.tests.testproject import views

urlpatterns = [
    url(r'^', include('ao.msazure.urls')),
    url(r'^', include('ao.upcloud.urls')),
    url('admin/', admin.site.urls),
    # url(r'^.*$', views.debug, name="debug"),
]
