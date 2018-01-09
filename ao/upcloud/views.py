import json
import sched

from django.http import HttpResponse, JsonResponse, Http404
from django.views.generic import View

from rest_framework import views
from rest_framework import viewsets
from rest_framework import decorators

from ao.core import utils
from . import settings
from . import models
from . import factories
from . import authentications
from . import permissions
from . import serializers
from . import exceptions


class APIViewSetMixin(object):
    authentication_classes = (authentications.UpCloudAuthentication,)
    permission_classes = (permissions.UpCloudPermission,)

    account_field = None

    def get_queryset(self):
        qs = self.queryset.all()
        if self.access_level > 0:
            qs = qs.filter(**{self.account_field: self.request.user})
        return qs

    def get_serializer(self, *args, **kwargs):
        if self.request.method == 'GET':
            if kwargs.get('many'):
                serializer_class = self.list_serializer_class
            else:
                serializer_class = self.retrieve_serializer_class
        elif self.request.method == 'POST':
            serializer_class = self.create_serializer_class
        elif self.request.method == 'PUT':
            serializer_class = self.update_serializer_class
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def get_serializer_context(self):
        return {
            'account': self.request.user,
        }

    def _get_factory_kwargs(self):
        kwargs = {}
        if self.account_field is not None:
            kwargs[self.account_field] = self.request.user
        return kwargs

    def get_object(self):
        try:
            obj = super(APIViewSetMixin, self).get_object()
        except Http404 as err:
            if self.access_level == 0:
                obj_attrs = self._get_factory_kwargs()
                obj_attrs.update(self.kwargs)
                obj = self.factory(**obj_attrs)
            else:
                raise
        return obj



class ServerViewSet(APIViewSetMixin, viewsets.ViewSet):
    access_level = settings.SERVER_ACCESS_LEVEL
    action_level = settings.SERVER_ACTION_LEVEL
    not_exist_exception = exceptions.ServerDoesNotExist
    not_forbidden_exception = exceptions.ServerForbidden

    def _get_server(self, pk=None):
        servers = models.Server.objects.filter(uuid=pk)
        exists = servers.exists()
        if self.access_level > 0:
            servers = servers.filter(account=self.request.user)
        server = servers.first()
        if server is None and self.access_level == 0:
            server = factories.ServerFactory(uuid=pk, account=self.request.user)
        return server, exists

    def list(self, request):
        data = {'servers': {'server': []}}
        servers = models.Server.objects.all()
        if self.access_level > 0:
            servers = servers.filter(account=self.request.user)
        data['servers']['server'] = [s.detail_format for s in servers]
        return JsonResponse(data)

    def create(self, request):
        serializer = serializers.PostServerSerializer(data=self.request.data)
        if serializer.is_valid():
            data = serializer.create(self.request.user)
            return views.Response(data, status=202)

    def retrieve(self, request, pk=None):
        server, exists = self._get_server(pk)
        try:
            self.check_object_permissions(request, (server, exists))
        except exceptions.APIException as err:
            return err.get_response()
        data = {'server': server.detail_format}
        return JsonResponse(data)

    @decorators.detail_route(
        methods=['post'],
        permission_classes=(permissions.ServerStoppedPermission,))
    def start(self, request, pk=None):
        server, exists = self._get_server(pk)
        # Check perms
        try:
            self.check_object_permissions(request, (server, exists))
        except exceptions.APIException as err:
            return err.get_response()
        # Run action delayed
        utils.delay(settings.SERVER_START_DELAY, server.start)
        # Response
        data = {'server': server.detail_format}
        return JsonResponse(data, status=200)

    @decorators.detail_route(
        methods=['post'],
        permission_classes=(permissions.ServerStartedPermission,))
    def stop(self, request, pk=None):
        server, exists = self._get_server(pk)
        # Check perms
        try:
            self.check_object_permissions(request, (server, exists))
        except exceptions.APIException as err:
            return err.get_response()
        # Run action delayed
        utils.delay(settings.SERVER_STOP_DELAY, server.stop)
        # Response
        data = {'server': server.detail_format}
        return JsonResponse(data, status=200)

    @decorators.detail_route(
        methods=['post'],
        permission_classes=(permissions.ServerStartedPermission,))
    def restart(self, request, pk=None):
        server, exists = self._get_server(pk)
        # Check perms
        try:
            self.check_object_permissions(request, (server, exists))
        except exceptions.APIException as err:
            return err.get_response()
        # Run action delayed
        utils.delay(settings.SERVER_STOP_DELAY, server.restart)
        # Response
        data = {'server': server.detail_format}
        return JsonResponse(data, status=200)

    @decorators.detail_route(
        methods=['post'],
        permission_classes=(permissions.ServerStoppedPermission,))
    def cancel(self, request, pk=None):
        server, exists = self._get_server(pk)
        # Check perms
        try:
            self.check_object_permissions(request, (server, exists))
        except exceptions.APIException as err:
            return err.get_response()
        server.delete()
        # Response
        return HttpResponse('', status=204)


class IpAddressViewSet(APIViewSetMixin, viewsets.ModelViewSet):
    queryset = models.IpAddress.objects.all()

    lookup_value_regex = '[0-9a-z:.]+'
    lookup_field = 'address'

    list_serializer_class = serializers.IpAddressListSerializer
    retrieve_serializer_class = serializers.IpAddressDetailSerializer
    create_serializer_class = serializers.PostIpAddressSerializer
    update_serializer_class = serializers.PutIpAddressSerializer

    access_level = settings.IP_ADDRESS_ACCESS_LEVEL
    action_level = settings.IP_ADDRESS_ACTION_LEVEL

    not_exist_exception = exceptions.IpAddressNotFound
    not_forbidden_exception = exceptions.IpAddressForbidden

    account_field = 'server__account'
    factory = factories.IpAddressFactory
