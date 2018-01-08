import uuid
import base64
import time
from django.db import models
from . import settings

STORAGE_TIERS = (
    ('hdd', 'hdd'),
    ('maxiops', 'maxiops'),
)
SERVER_STATES = (
    ('started', 'started'),
    ('stopped', 'stopped'),
    ('maintenance', 'maintenance'),
    ('error', 'error'),
)
SERVER_BOOT_ORDERS = (
    ('disk', 'disk'),
    ('cdrom', 'cdrom'),
    ('disk,cdrom', 'disk,cdrom'),
    ('cdrom,disk', 'cdrom,disk'),
)
NIC_MODELS = (
    ('e1000', 'e1000'),
    ('virtio', 'virtio'),
    ('rtl8139', 'rtl8139'),
)
STORAGE_STATES = IP_ACCESSES = (
    ('online', 'online'),
    ('maintenance', 'maintenance'),
    ('cloning', 'cloning'),
    ('backuping', 'backuping'),
    ('error', 'error'),
)
STORAGE_TYPES = (
    ('normal', 'normal'),
    ('backup', 'backup'),
    ('cdrom', 'cdrom'),
    ('template', 'template'),
)
STORAGE_ACCESS = (
    ('private', 'private'),
    ('public', 'public'),
)
BACKUP_RULE_INTERVALS = (
    ('daily', 'daily'),
    ('mon', 'mon'),
    ('tue', 'tue'),
    ('wed', 'wed'),
    ('thu', 'thu'),
    ('fri', 'fri'),
    ('sat', 'sat'),
    ('sun', 'sun'),
)
IP_FAMILIES = (
    ('IPv4', 'IPv4'),
    ('IPv6', 'IPv6'),
)

def on_off(value):
    return 'on' if value else 'off'


def yes_no(value):
    return 'yes' if value else 'no'


class Account(models.Model):
    credits = models.IntegerField()
    username = models.CharField(max_length=64)
    password = models.CharField(max_length=64)
    api_key = models.CharField(max_length=64, null=True, blank=True)

    class Meta:
        app_label = 'upcloud'

    def clean(self):
        key = '%s:%s' % (self.username, self.password)
        key = base64.b64encode(key)
        self.api_key = key


class Zone(models.Model):
    id = models.SlugField(primary_key=True)
    description = models.CharField(max_length=20)

    class Meta:
        app_label = 'upcloud'


class Plan(models.Model):
    name = models.CharField(max_length=64, primary_key=True)
    core_number = models.SmallIntegerField()
    memory_amount = models.SmallIntegerField()
    public_traffic_out = models.SmallIntegerField()
    storage_size = models.SmallIntegerField()
    storage_tier = models.CharField(max_length=7, choices=STORAGE_TIERS)

    class Meta:
        app_label = 'upcloud'


class Server(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    hostname = models.CharField(max_length=128)
    licence = models.SmallIntegerField(default=0, blank=True)
    plan = models.ForeignKey(Plan, null=True, blank=True)
    core_number = models.SmallIntegerField(blank=True)
    memory_amount = models.SmallIntegerField(blank=True)
    state = models.CharField(max_length=11, choices=SERVER_STATES)
    zone = models.ForeignKey(Zone)
    firewall = models.BooleanField(default=True, blank=True)
    boot_order = models.CharField(max_length=10, default='disk', blank=True)
    host = models.IntegerField()
    nic_model = models.CharField(max_length=7, default='e1000', choices=NIC_MODELS, blank=True)
    timezone = models.CharField(max_length=40)
    account = models.ForeignKey(Account, null=True, blank=True)

    class Meta:
        app_label = 'upcloud'

    @property
    def list_format(self):
        data = {
            'hostname': self.hostname,
            'licence': self.licence,
            'state': self.state,
            'title': self.title,
            'uuid': str(self.uuid),
            'zone': self.zone.id,
            'tags': {'tag': []},
        }
        if self.plan is not None:
            data.update(plan=self.plan.name,
                        core_number=self.plan.core_number,
                        memory_amount=self.plan.memory_amount,
                        plan_ivp4_bytes=0,
                        plan_ipv6_bytes=0)
        else:
            data.update(plan='custom',
                        core_number=self.core_number,
                        memory_amount=self.memory_amount)
        for tag in self.tag_set.all():
            data['tags']['tag'].append(tag.name)
        return data

    @property
    def detail_format(self):
        data = self.list_format.copy()
        data.update(boot_order=self.boot_order,
                    firewall=on_off(self.firewall),
                    host=self.host,
                    nic_model=self.nic_model,
                    storage_devices={'storage_device': []},
                    ip_addresses={'ip_address': []},
                    timezone=self.timezone,
                    # video_model=self.video_model,
                    # vnc=on_off(self.vnc),
                    # vnc_host=self.vnc_host,
                    # vnc_password=self.vnc_password,
                    # vnc_port=self.vnc_port,
                    )
        for storage in self.storage_set.all():
            storage_data = {
                'address': storage.address,
                'part_of_plan': yes_no(storage.part_of_plan),
                'storage': storage.id,
                'storage_size': storage.size,
                'storage_title': storage.title,
                'type': storage.type,
            }
            data['storage_devices']['storage_device'].append(storage_data)
        for ip in self.ipaddress_set.all():
            ip_data = {
                'access': ip.access,
                'address': ip.address,
                'family': ip.family,
            }
            data['ip_addresses']['ip_address'].append(ip_data)
        return data

    def start(self):
        self.state = 'started'
        self.save()

    def stop(self):
        self.state = 'stopped'
        self.save()

    def restart(self):
        self.stop()
        time.sleep(settings.SERVER_RESTART_DELAY)
        self.start()


class Tag(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    servers = models.ManyToManyField(Server)

    class Meta:
        app_label = 'upcloud'


class Storage(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64, null=True, blank=True)
    access = models.CharField(max_length=7, choices=STORAGE_ACCESS)
    type = models.CharField(max_length=8, choices=STORAGE_TYPES)
    tier = models.CharField(max_length=7, choices=STORAGE_TIERS)
    size = models.SmallIntegerField()
    part_of_plan = models.BooleanField()
    zone = models.ForeignKey(Zone)
    backup_rule_interval = models.CharField(max_length=5, choices=BACKUP_RULE_INTERVALS, null=True, blank=True)
    backup_rule_time = models.CharField(max_length=4, null=True, blank=True)
    backup_rule_retention = models.SmallIntegerField(null=True, blank=True)
    server = models.ForeignKey(Server, null=True, blank=True)
    state = models.CharField(max_length=11, choices=STORAGE_STATES)
    address = models.CharField(max_length=15, null=True, blank=True)
    favorite = models.BooleanField(default=False)
    account = models.ForeignKey(Account, null=True, blank=True)

    class Meta:
        app_label = 'upcloud'


class IpAddress(models.Model):
    access = models.CharField(max_length=7, choices=IP_ACCESSES)
    address = models.GenericIPAddressField()
    family = models.CharField(max_length=4, choices=IP_FAMILIES)
    part_of_plan = models.BooleanField()
    hostname = models.CharField(max_length=128)
    server = models.ForeignKey(Server, null=True, blank=True)
    account = models.ForeignKey(Account, null=True, blank=True)

    class Meta:
        app_label = 'upcloud'
