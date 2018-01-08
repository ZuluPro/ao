from rest_framework import fields
from rest_framework import serializers
from . import settings
from . import models
from . import factories


class BoolField(serializers.Field):
    def to_representation(self, obj):
        return self.TRUE if obj else self.FALSE

    def to_internal_value(self, data):
        if data == self.TRUE:
            return True
        elif data == self.FALSE:
            return False
        return


class OnOffField(BoolField):
    TRUE = 'on'
    FALSE = 'off'


class YesNoField(BoolField):
    TRUE = 'yes'
    FALSE = 'no'


class SshKeyField(fields.CharField):
    pass

    def create(self, *args, **kwargs):
        pass

class SshKeyListField(fields.ListField):
    child = SshKeyField()

    def create(self, *args, **kwargs):
        pass


class ServerIpsSerializer(serializers.Serializer):
    access = fields.ChoiceField(choices=models.IP_ACCESSES)
    family = fields.ChoiceField(choices=models.IP_FAMILIES, default='ipv4')

    def create(self, *args, **kwargs):
        pass


class ServerIpSerializer(serializers.Serializer):
    ip_address = ServerIpsSerializer(many=True)

    def create(self, *args, **kwargs):
        pass


class SshKeyListSerializer(serializers.Serializer):
    ssh_key = SshKeyListField()

    def create(self, *args, **kwargs):
        pass


class ServerLoginUserSerializer(serializers.Serializer):
    create_password = YesNoField(default='yes')
    username = fields.CharField(default='root')
    ssh_keys = SshKeyListSerializer()

    def create(self, *args, **kwargs):
        pass


STORAGE_ACTIONS = ('create', 'clone', 'attach')
STORAGE_TYPES = ('disk', 'cdrom')
class ServerStorageDeviceSerializer(serializers.Serializer):
    action = fields.ChoiceField(choices=STORAGE_ACTIONS)
    address = fields.CharField(required=False)
    size = fields.IntegerField(min_value=10, max_value=1024)
    tier = fields.ChoiceField(choices=models.STORAGE_TIERS, default='hdd', required=False)
    title = fields.CharField(required=False)
    type = fields.ChoiceField(choices=STORAGE_TYPES, default='disk', required=False)

    storage = fields.CharField()

    def validate_storage(self, value):
        exists = models.Storage.objects.filter(uuid=value).exists()
        if exists:
            pass 
        elif not exists and settings.CREATION_LEVEL == 0:
            value = factories.StorageFactory(uuid=value).uuid
        return value

    def create(self, *args, **kwargs):
        pass

class ServerStorageDeviceListSerializer(serializers.Serializer):
    storage_device = ServerStorageDeviceSerializer(many=True)

    def create(self, *args, **kwargs):
        pass


PASSWORD_DELIVERIES = ('none', 'email', 'sms')
class ServerSerializer(serializers.ModelSerializer):
    firewall = OnOffField(required=False)
    timezone = fields.CharField(required=False)
    ip_addresses = ServerIpSerializer(required=False)
    login_user = ServerLoginUserSerializer(required=False)
    storage_devices = ServerStorageDeviceListSerializer(required=False)
    password_delivery = fields.ChoiceField(choices=PASSWORD_DELIVERIES, default='none', required=False)

    class Meta:
        model = models.Server
        exclude = ('host', 'state')

    def validate_plan(self, value):
        if value == 'custom':
            return None
        exists = models.Plan.objects.filter(name=value).exists()
        if exists:
            pass 
        elif not exists and settings.CREATION_LEVEL == 0:
            value = factories.PlanFactory(name=value)
        else:
            raise serializers.ValidationError('')
        return value

    def validate_zone(self, value):
        exists = models.Zone.objects.filter(id=value).exists()
        if exists:
            pass 
        elif not exists and settings.CREATION_LEVEL == 0:
            value = factories.ZoneFactory(id=value)
        else:
            raise serializers.ValidationError('')
        return value


class PostServerSerializer(serializers.Serializer):
    server = ServerSerializer()

    def create(self, account, *args, **kwargs):
        server_data = self.validated_data['server']
        login_user = server_data.pop('login_user', None)
        storage_devices = server_data.pop('storage_devices', None)
        password_delivery = server_data.pop('password_delivery', None)
        if settings.CREATION_LEVEL == 0:
            instance = factories.ServerFactory(**server_data)
        else:
            instance = models.Server.objects.create(**server_data)
        return {'server': instance.detail_format}


STOP_TYPES = ('soft', 'hard')
class StopServerSerializer(serializers.Serializer):
    stop_type = fields.ChoiceField(STOP_TYPES, required=False, default='soft')
    timeout = fields.IntegerField(min_value=1, max_value=600, required=False, default='1')


class PostStopServerSerializer(serializers.Serializer):
    stop_server = StopServerSerializer()


TIMEOUT_ACTIONS = ('destroy', 'ignore')
class RestartServerSerializer(StopServerSerializer):
    timeout_action = fields.ChoiceField(TIMEOUT_ACTIONS, required=False, default='ignore')


class PostRestartServerSerializer(serializers.Serializer):
    restart_server = RestartServerSerializer()
