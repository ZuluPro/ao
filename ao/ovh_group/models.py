import uuid
from django.db import models

FLAVOR_TYPES = (
    ('ovh.ssd.eg', 'ovh.ssd.eg'),
    ('ovh.ssd.cpu', 'ovh.ssd.cpu'),
    ('ovh.ceph.eg', 'ovh.ceph.eg'),
    ('ovh.cpu', 'ovh.cpu'),
    ('ovh.ssd.ram', 'ovh.ssd.ram'),
    ('ovh.vps-ssd', 'ovh.vps-ssd'),
    ('ovh.ram', 'ovh.ram'),
)
OS_TYPES = (
    ('linux', 'linux'),
    ('windows', 'windows'),
)
VISIBILITY = (
    ('private', 'private'),
    ('public', 'public'),
)
IMAGE_STATUS = (
    ('active', 'active'),
)
IP_TYPES = (
    ('private', 'private'),
    ('public', 'public'),
)
IP_STATUS = (
    ('active', 'active'),
)
INSTANCE_STATUS = (
    ('active', 'active'),
)


class Account(models.Model):
    username = models.CharField(max_length=30, primary_key=True)


class Service(models.Model):
    id = models.CharField(max_length=32, primary_key=True)
    description = models.TextField(max_length=1000)
    creation_date = models.DateTimeField()


class Region(models.Model):
    id = models.CharField(max_length=5, primary_key=True)
    continent_code = models.CharField(max_length=3)
    datacenter_location = models.CharField(max_length=3)
    name = models.CharField(max_length=20)

    volume = models.CharField(max_length=10, default='UP')
    image = models.CharField(max_length=10, default='UP')
    network = models.CharField(max_length=10, default='UP')
    instance = models.CharField(max_length=10, default='UP')


class Flavor(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    region = models.ForeignKey(Region)
    name = models.CharField(max_length=50)

    type = models.CharField(max_length=20, choices=FLAVOR_TYPES)
    os_type = models.CharField(max_length=20, choices=OS_TYPES)
    vcpus = models.PositiveSmallIntegerField()
    ram = models.PositiveSmallIntegerField()
    disk = models.PositiveSmallIntegerField()
    outbound_bandwidth = models.PositiveSmallIntegerField()
    inbound_bandwidth = models.PositiveSmallIntegerField()

    available = models.BooleanField(default=True)


class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    user = models.CharField(max_length=20)
    name = models.CharField(max_length=64)
    type = models.CharField(max_length=20, choices=OS_TYPES)

    visibility = models.CharField(max_length=7, choices=VISIBILITY)
    flavor_type = models.CharField(max_length=20, choices=FLAVOR_TYPES, null=True, blank=True)
    status = models.CharField(max_length=15, choices=IMAGE_STATUS, default='active')
    region = models.ForeignKey(Region)
    plan_code = models.CharField(max_length=64, blank=True, null=True)

    min_disk = models.PositiveSmallIntegerField(default=0)
    min_ram = models.PositiveSmallIntegerField(default=0)
    size = models.FloatField()

    creation_date = models.DateTimeField()


class SshKey(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    name = models.CharField(max_length=64)
    regions = models.ManyToManyField(Region)
    public = models.TextField(max_length=2000)


class IpAddress(models.Model):
    id = models.CharField(max_length=24, primary_key=True)
    type = models.CharField(max_length=24, choices=IP_TYPES)
    status = models.CharField(max_length=24, choices=IP_STATUS)
    ip = models.GenericIPAddressField()


class Instance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=64)
    region = models.ForeignKey(Region)

    flavor = models.ForeignKey(Flavor)
    image = models.ForeignKey(Image)
    plan_code = models.CharField(max_length=64, blank=True, null=True)

    status = models.CharField(max_length=20, choices=INSTANCE_STATUS)
    created = models.DateTimeField()
    ssh_key = models.ForeignKey(SshKey, null=True, blank=True)
    monthly_billing = models.BooleanField(default=False)
    ip_addresses = models.ManyToManyField(IpAddress, blank=True)
