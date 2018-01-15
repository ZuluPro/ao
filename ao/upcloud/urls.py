from django.conf.urls import url
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter(trailing_slash=False)
router.register(r'[0-9\.]*/server', views.ServerViewSet, base_name='server')
router.register(r'[0-9\.]*/ip_address', views.IpAddressViewSet, base_name='ip_address')
router.register(r'[0-9\.]*/storage', views.StorageViewSet, base_name='storage')

urlpatterns = router.urls
