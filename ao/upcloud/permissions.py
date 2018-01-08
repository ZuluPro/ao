from rest_framework import permissions
from . import settings
from . import exceptions


class UpCloudPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        if settings.AUTHENTICATION_LEVEL > 0:
            pass
        return True

    def has_object_permission(self, request, view, obj):
        if isinstance(obj, (list, tuple)):
            obj, exists = obj
        else:
            obj, exists = obj, True

        if view.access_level == 0:
            return True

        if obj is None and not exists:
            raise view.not_exist_exception()

        if obj is None and exists:
            raise view.not_forbidden_exception()

        return request.user == obj.account


class ServerStatePermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, (list, tuple)):
            server, exists = obj
        else:
            server, exists = obj, True

        if server.state != self.state and view.action_level > 0:
            raise exceptions.ServerStateIllegal()

        return True


class ServerStoppedPermission(ServerStatePermission):
    state = 'stopped'


class ServerStartedPermission(ServerStatePermission):
    state = 'stopped'
