import json
import sched

from django.http import HttpResponse, JsonResponse
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


class AuthenticationFailedResponse(JsonResponse):
    def __init__(self, data=None, *args, **kwargs):
        data = {
            "error": {
                "error_code": "AUTHENTICATION_FAILED",
                "error_message": "Authentication failed using the given username and password."
            }
        }
        super(AuthenticationFailedResponse, self).__init__(data=data,
                                                           *args, **kwargs)
        self.status_code = 401


class BadRequestResponse(JsonResponse):
    def __init__(self, err_code, err_message, data=None, *args, **kwargs):
        data = {
            "error": {
                "error_code": err_code,
                "error_message": err_message,
            }
        }
        super(BadRequestResponse, self).__init__(data=data, *args, **kwargs)
        self.status_code = 400


class APIViewSet(viewsets.ViewSet):
    authentication_classes = (authentications.UpCloudAuthentication,)
    permission_classes = (permissions.UpCloudPermission,)


class ServerViewSet(APIViewSet):
    access_level = settings.SERVER_ACCESS_LEVEL
    action_level = settings.SERVER_ACTION_LEVEL
    not_exist_exception = exceptions.ServerDoesNotExist
    not_forbidden_exception = exceptions.ServerForbidden

    def list(self, request):
        data = {'servers': {'server': []}}
        servers = models.Server.objects.all()
        if self.access_level > 0:
            account = servers.filter(account=self.user)
        data['servers']['server'] = [s.detail_format for s in servers]
        return JsonResponse(data)

    def create(self, request):
        serializer = serializers.PostServerSerializer(data=self.request.data)
        if serializer.is_valid():
            data = serializer.create(self.request.user)
            return views.Response(data, status=202)

    def _get_server(self, pk=None):
        servers = models.Server.objects.filter(uuid=pk)
        exists = servers.exists()
        if self.access_level > 0:
            servers = servers.filter(account=self.request.user)
        server = servers.first()
        if server is None and self.access_level == 0:
            server = factories.ServerFactory(uuid=pk, account=self.request.user)
        return server, exists

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
