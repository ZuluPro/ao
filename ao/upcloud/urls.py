from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'[0-9\.]*/server', views.ServerViewSet, base_name='server')
router.register(r'[0-9\.]*/ip_address', views.IpAddressViewSet, base_name='ip_address')
router.register(r'[0-9\.]*/storage', views.StorageViewSet, base_name='storage')

urlpatterns = [
    url(r'^[0-9\.]*/account', views.AccountView.as_view(), name='account'),
    url(r'^[0-9\.]*/price', views.PriceView.as_view(), name='price'),
    url(r'^[0-9\.]*/zone', views.ZoneView.as_view(), name='zone'),
    url(r'^[0-9\.]*/timezone', views.TimezoneView.as_view(), name='timezone'),
    url(r'^[0-9\.]*/plan', views.PlanView.as_view(), name='plan'),
]

urlpatterns += router.urls
