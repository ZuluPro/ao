import uuid
import base64
import time

from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

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
STORAGE_STATES = (
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
STORAGE_ACCESS = IP_ACCESSES = (
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


def random_host_id():
    return random.randint(1, 10**10)


class Server(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64)
    hostname = models.CharField(max_length=128)
    licence = models.SmallIntegerField(default=0, blank=True)
    plan = models.ForeignKey(Plan, null=True, blank=True)
    core_number = models.SmallIntegerField(blank=True)
    memory_amount = models.SmallIntegerField(blank=True)
    state = models.CharField(max_length=11, choices=SERVER_STATES, default='started', blank=True)
    zone = models.ForeignKey(Zone)
    firewall = models.BooleanField(default=True, blank=True)
    boot_order = models.CharField(max_length=10, default='disk', blank=True)
    host = models.IntegerField(blank=True, default=random_host_id)
    nic_model = models.CharField(max_length=7, default='e1000', choices=NIC_MODELS, blank=True)
    timezone = models.CharField(max_length=40)
    account = models.ForeignKey(Account, null=True, blank=True)

    class Meta:
        app_label = 'upcloud'

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


@receiver(post_save, sender=Server)
def server_post_save(sender, instance, created, raw, using, update_fields, **kwargs):
    if created:
        if instance.plan:
            Storage.objects.create(
                title='Operating system disk',
                access='private',
                type='disk',
                tier=instance.plan.storage_tier,
                size=instance.plan.storage_size,
                part_of_plan=True,
                zone=instance.zone,
                server=instance,
                state='online',
                address='ide:0:1',
                account=instance.account)
        else:
            instance.core_number = instance.plan.core_number
            instance.memory_amount = instance.plan.memory_amount



class Tag(models.Model):
    name = models.CharField(max_length=32)
    description = models.CharField(max_length=255)
    servers = models.ManyToManyField(Server)

    class Meta:
        app_label = 'upcloud'


class Storage(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=64, null=True, blank=True)
    access = models.CharField(max_length=7, choices=STORAGE_ACCESS, blank=True)
    type = models.CharField(max_length=8, choices=STORAGE_TYPES, blank=True)
    tier = models.CharField(max_length=7, choices=STORAGE_TIERS, blank=True, default='hdd')
    size = models.SmallIntegerField()
    license = models.SmallIntegerField(default=0, blank=True)
    part_of_plan = models.BooleanField()
    zone = models.ForeignKey(Zone, blank=True)
    backup_rule_interval = models.CharField(max_length=5, choices=BACKUP_RULE_INTERVALS, null=True, blank=True)
    backup_rule_time = models.CharField(max_length=4, null=True, blank=True)
    backup_rule_retention = models.SmallIntegerField(null=True, blank=True)
    backup_of = models.ForeignKey('self', null=True, blank=True)
    server = models.ForeignKey(Server, null=True, blank=True)
    state = models.CharField(max_length=11, choices=STORAGE_STATES, default='maintenance', blank=True)
    address = models.CharField(max_length=15, null=True, blank=True)
    favorite = models.BooleanField(default=False)
    account = models.ForeignKey(Account, null=True, blank=True)

    class Meta:
        app_label = 'upcloud'

    def initialize(self):
        self.state = 'online'
        self.save()

    def initialize_backup(self, origin_uuid):
        self.state = 'online'
        self.backup_of = Storage.objects.get(uuid=origin_uuid)
        self.save()

    def initialize_template(self):
        self.state = 'online'
        self.save()


class IpAddress(models.Model):
    address = models.GenericIPAddressField(primary_key=True)
    access = models.CharField(max_length=7, choices=IP_ACCESSES)
    family = models.CharField(max_length=4, choices=IP_FAMILIES)
    part_of_plan = models.BooleanField(default=False, blank=True)
    ptr_record = models.CharField(max_length=128)
    server = models.ForeignKey(Server)

    class Meta:
        app_label = 'upcloud'
        verbose_name = 'IP address'
        verbose_name_plural = 'IP addresses'
