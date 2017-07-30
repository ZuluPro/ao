from django.conf.urls import include, url
from ao.tests.testproject import views

urlpatterns = [
    url(r'^', include('ao.msazure.urls')),
    url(r'^.*$', views.debug, name="debug"),
]
