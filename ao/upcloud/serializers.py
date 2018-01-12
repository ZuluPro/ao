from rest_framework import serializers
from rest_framework import fields

from ao.core import fields as ao_fields
from ao.core import utils
from . import settings
from . import models
from . import factories


class SerializerMixin(object):
    def __init__(self, *args, **kwargs):
        self.account = kwargs.pop('account', None)
        super(SerializerMixin, self).__init__(*args, **kwargs)
    

class ListIpAddressSerializer(serializers.ListSerializer):
    """list serializer"""
    def to_representation(self, instance):
        data = super(ListIpAddressSerializer, self).to_representation(instance)
        data = {'ip_addresses': {'ip_address': data}}
        return data

    @property
    def data(self):
        super(ListIpAddressSerializer, self).data
        return self._data


class IpAddressSerializer(serializers.ModelSerializer):
    part_of_plan = ao_fields.YesNoField(required=False)
    server = serializers.PrimaryKeyRelatedField(queryset=models.Server.objects.all(), required=False)

    action_level = settings.IP_ADDRESS_ACTION_LEVEL

    class Meta:
        model = models.IpAddress
        fields = '__all__'

    def validate_server(self, value):
        exists = models.Server.objects.filter(uuid=value.uuid).exists()
        if exists:
            value = str(models.Server.objects.get(uuid=value.uuid).uuid)
        elif not exists and self.action_level == 0:
            value = str(factories.ServerFactory(uuid=value.uuid).uuid)
        else:
            raise serializers.ValidationError('')
        return value

    def to_representation(self, instance):
        data = super(IpAddressSerializer, self).to_representation(instance)
        return data


class IpAddressListSerializer(IpAddressSerializer):
    part_of_plan = ao_fields.YesNoField(required=False, write_only=True)

    class Meta:
        model = models.IpAddress
        fields = '__all__'
        list_serializer_class = ListIpAddressSerializer


class IpAddressDetailSerializer(IpAddressSerializer):
    class Meta:
        model = models.IpAddress
        fields = '__all__'

    def to_representation(self, instance):
        data = super(IpAddressDetailSerializer, self).to_representation(instance)
        data = {'ip_address': data}
        return data


class CreateIpAddressSerializer(IpAddressSerializer):
    class Meta:
        model = models.IpAddress
        fields = ('family', 'access', 'server')
    

class PostIpAddressSerializer(SerializerMixin, serializers.Serializer):
    ip_address = CreateIpAddressSerializer()

    def save(self, *args, **kwargs):
        ip_data = self.validated_data['ip_address']
        if settings.IP_ADDRESS_ACTION_LEVEL == 0:
            server = models.Server.objects.filter(uuid=ip_data.pop('server')).first()
            ip_data.update(server=server,
                           server__account=self.account)
            instance = factories.IpAddressFactory(**ip_data)
        else:
            # TODO: Manage public/private
            address = factories.fake.ipv4() if ip_data['family'] == 'IPV4' else factories.fake.ipv6()
            ptr_record = '%s.v6.zone.host.upcloud.com' % factories.fake.user_name()
            ip_data.update(address=address,
                           part_of_plan=False,
                           ptr_record=ptr_record)
            instance = IpAddress.objets.create(**ip_data)
            instance.family = factories.make_ip_family(instance)
        return instance


class ModifyIpAddressSerializer(IpAddressSerializer):
    class Meta:
        model = models.IpAddress
        fields = ('ptr_record',)

    def update(self, *args, **kwargs):
        pass
    

class PutIpAddressSerializer(SerializerMixin, serializers.Serializer):
    ip_address = ModifyIpAddressSerializer()

    def save(self, *args, **kwargs):
        self.instance.ptr_record = self.validated_data['ip_address']['ptr_record']
        self.instance.save()
        return self.instance

    @property
    def data(self):
        serializer = IpAddressListSerializer(self.instance)
        return serializer.data


class ListStorageSerializer(serializers.ListSerializer):
    """list serializer"""
    def to_representation(self, instance):
        data = super(ListServerSerializer, self).to_representation(instance)
        data = {'storage_devices': {'storage_device': data}}
        return data

    @property
    def data(self):
        super(ListStorageSerializer, self).data
        return self._data


class ServerStorageSerializer(serializers.ModelSerializer):
    part_of_plan = ao_fields.YesNoField(required=False)
    server = serializers.PrimaryKeyRelatedField(queryset=models.Server.objects.all(), required=False)

    class Meta:
        model = models.Storage
        fields = '__all__'
        list_serializer_class = ListStorageSerializer

    def to_internal_data(self, data):
        data = data['storage_device']
        return super(ServerStorageSerializer, self).to_internal_data(data)


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
    ssh_key = ao_fields.SshKeyListField()

    def create(self, *args, **kwargs):
        pass


class ServerLoginUserSerializer(serializers.Serializer):
    create_password = ao_fields.YesNoField(default='yes')
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


class ListServerSerializer(serializers.ListSerializer):
    """list serializer"""
    def to_representation(self, instance):
        data = super(ListServerSerializer, self).to_representation(instance)
        data = {'servers': {'server': data}}
        return data

    @property
    def data(self):
        super(ListServerSerializer, self).data
        return self._data


PASSWORD_DELIVERIES = ('none', 'email', 'sms')
class ServerSerializer(serializers.ModelSerializer):
    firewall = ao_fields.OnOffField(required=False)
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


class ServerListSerializer(ServerSerializer):
    """ListView Serializer"""
    class Meta:
        model = models.Server
        exclude = ('account',)
        list_serializer_class = ListServerSerializer


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


class ServerListIpAddressesSerializer(serializers.ListSerializer):
    def to_representation(self, instance):
        data = super(ServerListIpAddressesSerializer, self).to_representation(instance)
        return {'ip_address': data}


class ServerIpAddressesSerializer(IpAddressSerializer):
    class Meta:
        model = models.IpAddress
        fields = ('access', 'address', 'family')
        list_serializer_class = ServerListIpAddressesSerializer

    def to_internal_value(self, data):
        data = data['ip_address']
        return super(ServerIpAddressesSerializer, self).to_internal_value(data)


class ServerListStorageSerializer(serializers.ListSerializer):
    def to_representation(self, instance):
        data = super(ServerListStorageSerializer, self).to_representation(instance)
        return {'storage_device': data}

    def to_internal_value(self, data):
        data = data['storage_device']
        return super(ServerListStorageSerializer, self).to_internal_value(data)


class ServerStoragesSerializer(ServerStorageSerializer):
    storage = fields.UUIDField(source='uuid')
    storage_size = fields.IntegerField(source='size')
    storage_title = fields.CharField(source='title')

    class Meta:
        model = models.Storage
        list_serializer_class = ServerListStorageSerializer
        fields = ('part_of_plan', 'address', 'storage', 'storage_size', 'storage_title', 'type')



class ServerDetailSerializer(ServerSerializer):
    ip_addresses = ServerIpAddressesSerializer(source='ipaddress_set', many=True, required=False)
    storage_devices = ServerStoragesSerializer(source='storage_set', many=True, required=False)

    class Meta:
        model = models.Server
        fields = (
            'uuid',
            'title',
            'hostname',
            'licence',
            'plan',
            'core_number',
            'memory_amount',
            'state',
            'zone',
            'firewall',
            'boot_order',
            'host',
            'nic_model',
            'timezone',
            'ip_addresses',
            'storage_devices',
        )

    def to_representation(self, instance):
        data = super(ServerDetailSerializer, self).to_representation(instance)
        data = {'server': data}
        return data

    def to_internal_value(self, data):
        data = data['server']
        return super(ServerDetailSerializer, self).to_internal_value(data)


class PostServerStorageSerializer(ServerStorageSerializer):
    class Meta:
        model = models.Storage
        list_serializer_class = ListStorageSerializer
        fields = (
            # 'action',
            'address',
            'size',
            # 'storage',
            'tier',
            'title',
            'type',
        )


class PostServerSerializer(ServerDetailSerializer):
    storage_devices = PostServerStorageSerializer(many=True, required=False)

    def _clone_storage(self, server, storage_device):
        base_storage = models.Storage.objects.filter(uuid=storage_device['storage']).first()
        if settings.STORAGE_ACTION_LEVEL == 0:
            if base_storage is None:
                base_storage = factories.StorageFactory(
                    access='private',
                    type='disk',
                    part_of_plan=False,
                    zone=server.zone,
                    account=server.account)
            base_storage.uuid = None
            base_storage.server = server
            base_storage.state = 'maintenance'
            base_storage.save()
            storage = base_storage
        return storage
                    

    def _create_storage(self, server, storage_device):
        storage = models.Storage.objects.create(
            title=storage_device['title'],
            access='private',
            type=storage_device.get('type', 'disk'),
            tier=storage_device['tier'],
            size=storage_device['size'],
            part_of_plan=False,
            zone=server.zone,
            server=server,
            address=storage_device.get('address', ''),
            account=server.account)
        return storage

    def _attach_storage(self, server, storage_device):
        storage = models.Storage.objects.filter(uuid=storage_device['storage']).first()
        if storage is None and settings.STORAGE_ACTION_LEVEL == 0:
            storage = factories.StorageFactory(
                access='private',
                type='disk',
                part_of_plan=False,
                zone=server.zone,
                account=server.account)
        return storage

    def create(self, *args, **kwargs):
        server_data = self.validated_data.copy()
        login_user = server_data.pop('login_user', None)
        storage_devices = server_data.pop('storage_devices', None)
        password_delivery = server_data.pop('password_delivery', None)
        # Server
        if settings.SERVER_ACTION_LEVEL == 0:
            server = factories.ServerFactory(
                account=self.account,
                state='started',
                **server_data)
        else:
            server = models.Server.objects.create(
                account=self.account,
                **server_data)
        # Storages
        for storage_device in storage_devices:
            if storage['action'] == 'clone':
                storage = self._clone_storage(server, storage_device)
            elif storage['action'] == 'create':
                storage = self._create_storage(server, storage_device)
            elif storage['action'] == 'attach':
                storage = self._attach_storage(server, storage_device)
        # IPs
        return server


class StorageSerializer(serializers.ModelSerializer):
    """Base Storage Serializer"""
    server = serializers.PrimaryKeyRelatedField(queryset=models.Server.objects.all(), required=False)

    class Meta:
        model = models.Storage
        exclude = (
            'backup_rule_interval',
            'backup_rule_time',
            'backup_rule_retention',
            'backup_of',
            'favorite',
            'account',
            'server',
            'address',
            'part_of_plan',
        )

    def to_internal_data(self, data):
        data = data['storage']
        backup_rule = data.pop('backup_rules', None)
        if backup_rule:
            data.update(backup_rule_interval=backup_rule['interval'],
                        backup_rule_time=backup_rule['time'],
                        backup_rule_retention=backup_rule['retention'])
        return super(StorageSerializer, self).to_internal_data(data)

    def to_representation(self, instance, detail=True):
        data = super(StorageSerializer, self).to_representation(instance)
        data.update(uuid=str(instance.uuid),
                    state=instance.state)
        if detail:
            # Backup rule
            if instance.backup_rule_time and instance.type == 'disk':
                backup_rule = {
                    'interval': instance.backup_rule_interval,
                    'time': instance.backup_rule_time,
                    'retention': instance.backup_rule_retention,
                }
            else:
                backup_rule = ''
            data.pop('backup_rule_interval', None)
            data.pop('backup_rule_time', None)
            data.pop('backup_rule_retention', None)
            data['backup_rule'] = backup_rule
            # Backup
            backups = data.pop('backup', [])
            data['backups'] = {'backups': backups}
            # Server
            data['servers'] = {'server': []}
            server_uuid = data.pop('server', None)
            if server_uuid is not None:
                data['servers']['server'] = [server_uuid]
            # Format
            data = {'storage': data}
        return data


class ListStorageSerializer(serializers.ListSerializer):
    def to_representation(self, instance):
        data = super(ListStorageSerializer, self).to_representation(instance)
        data = {'storages': {'storage': data}}
        return data

    @property
    def data(self):
        super(ListStorageSerializer, self).data
        return self._data


class StorageListSerializer(StorageSerializer):
    """List Storage Serializer"""
    class Meta:
        model = models.Storage
        list_serializer_class = ListStorageSerializer
        fields = (
            'access',
            'license',
            'size',
            'state',
            'tier',
            'title',
            'type',
            'uuid',
            'zone',
        )

    def to_representation(self, instance):
        data = super(StorageListSerializer, self).to_representation(instance, False)
        return data


class StorageCreateSerializer(StorageSerializer):
    class Meta:
        model = models.Storage
        fields = (
            'size',
            'tier',
            'title',
            'zone',
            'backup_rule_interval',
            'backup_rule_time',
            'backup_rule_retention',
        )

    def validate_empty_values(self, data):
        data = data.get('storage')
        return super(StorageCreateSerializer, self).validate_empty_values(data)

    def save(self, *args, **kwargs):
        storage_data = self.validated_data
        storage_data.update(account=self.account,
                            state='maintenance',
                            type='disk')
        if settings.STORAGE_ACTION_LEVEL == 0:
            self.instance = factories.StorageFactory(**storage_data)
        else:
            # TODO: Check
            self.instance = super(StorageCreateSerializer, self).save(*args, **kwargs)
        utils.delay(setings.STORAGE_INITIALIZE_DELAY, self.instance.initialize)
        return self.instance


class StorageUpdateSerializer(StorageSerializer):
    class Meta:
        model = models.Storage
        fields = (
            'size',
            'title',
            'backup_rule_interval',
            'backup_rule_time',
            'backup_rule_retention',
        )

    def validate_empty_values(self, data):
        data = data.get('storage')
        return super(StorageUpdateSerializer, self).validate_empty_values(data)

    def update(self, instance, validated_data):
        storage_data = validated_data.copy()
        storage_data.update(account=self.account,
                            state='maintenance',
                            type='disk')
        update_func = models.Storage.objects.filter(uuid=self.instance.uuid).update
        # TODO: Validation
        if settings.STORAGE_ACTION_LEVEL > 0:
            pass
        utils.delay(setings.STORAGE_MODIFY_DELAY, update_func, **storage_data)
        return self.instance
