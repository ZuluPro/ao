import base64
import random
import ipaddress
import faker
import factory
from factory import fuzzy
from ao.upcloud import models

fake = faker.Faker()

STORAGE_ACCESS = [i for i, j in models.STORAGE_ACCESS]
STORAGE_TIERS = [i for i, j in models.STORAGE_TIERS]
STORAGE_TYPES = [i for i, j in models.STORAGE_TYPES]
BACKUP_RULE_INTERVALS = [i for i, j in models.BACKUP_RULE_INTERVALS]
FIREWALL_RULE_ACTIONS = [i for i, j in models.FIREWALL_RULE_ACTIONS]
FIREWALL_RULE_DIRECTIONS = [i for i, j in models.FIREWALL_RULE_DIRECTIONS]
FIREWALL_RULE_PROTOCOLS = [i for i, j in models.FIREWALL_RULE_PROTOCOLS]

def make_api_key(username, password):
    key = bytes('%s:%s' % (username, password), 'ascii')
    key = base64.b64encode(key)
    return key


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'upcloud.Account'

    credits = fuzzy.FuzzyInteger(1, 10**4)
    username = factory.Faker('user_name')
    password = factory.Faker('password')
    api_key = factory.LazyAttribute(lambda a: make_api_key(a.username, a.password))


class ZoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'upcloud.Zone'

    description = factory.Faker('city')
    id = factory.LazyAttribute(lambda a: fake.slug(a.description))

    firewall_price = fuzzy.FuzzyDecimal(0.1, 1)

    io_request_backup_price = fuzzy.FuzzyDecimal(0.1, 1)
    io_request_hdd_price = fuzzy.FuzzyDecimal(0.1, 1)
    io_request_maxiops_price = fuzzy.FuzzyDecimal(0.1, 1)
    ipv4_address_price = fuzzy.FuzzyDecimal(0.1, 1)
    ipv6_address_price = fuzzy.FuzzyDecimal(0.1, 1)
    public_ipv4_bandwidth_in_price = fuzzy.FuzzyDecimal(0.1, 1)
    public_ipv4_bandwidth_out_price = fuzzy.FuzzyDecimal(0.1, 1)
    public_ipv6_bandwidth_in_price = fuzzy.FuzzyDecimal(0.1, 1)
    public_ipv6_bandwidth_out_price = fuzzy.FuzzyDecimal(0.1, 1)
    server_core_price = fuzzy.FuzzyDecimal(0.1, 1)
    server_memory_price = fuzzy.FuzzyDecimal(0.1, 1)
    storage_backup_price = fuzzy.FuzzyDecimal(0.1, 1)
    storage_hdd_price = fuzzy.FuzzyDecimal(0.1, 1)
    storage_maxiops_price = fuzzy.FuzzyDecimal(0.1, 1)

    plan_1cpu_price = fuzzy.FuzzyDecimal(0.1, 1)
    plan_2cpu_price = fuzzy.FuzzyDecimal(0.1, 1)
    plan_4cpu_price = fuzzy.FuzzyDecimal(0.1, 1)
    plan_6cpu_price = fuzzy.FuzzyDecimal(0.1, 1)
    plan_8cpu_price = fuzzy.FuzzyDecimal(0.1, 1)
    plan_12cpu_price = fuzzy.FuzzyDecimal(0.1, 1)
    plan_16cpu_price = fuzzy.FuzzyDecimal(0.1, 1)
    plan_20cpu_price = fuzzy.FuzzyDecimal(0.1, 1)

    windows_standard_price = fuzzy.FuzzyDecimal(0.1, 1)
    windows_datacenter_price = fuzzy.FuzzyDecimal(0.1, 1)


class PlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'upcloud.Plan'

    name = factory.LazyAttribute(lambda a: '%dxCPU-%dGB' % (a.core_number, a.memory_amount/1024))
    core_number = fuzzy.FuzzyInteger(1, 16, 2)
    memory_amount = fuzzy.FuzzyInteger(1024, 2**20*32, 1024)
    public_traffic_out = 0
    storage_size = fuzzy.FuzzyInteger(10, 1024)
    storage_tier = fuzzy.FuzzyChoice(models.STORAGE_TIERS)


def make_core_number(server):
    if server.plan is None:
        return fuzzy.FuzzyInteger(1, 16, 2)
    return server.plan.core_number


def make_memory_amount(server):
    if server.plan is None:
        return fuzzy.FuzzyInteger(1024, 2**20*32, 1024)
    return server.plan.memory_amount


SERVER_STATES = [i for i, j in models.SERVER_STATES]
SERVER_BOOT_ORDERS = [i for i, j in models.SERVER_BOOT_ORDERS]
class ServerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'upcloud.Server'

    title = factory.Faker('name')
    hostname = factory.Faker('domain_name')
    licence = 0
    state = fuzzy.FuzzyChoice(SERVER_STATES)
    zone = factory.SubFactory(ZoneFactory)
    firewall = fuzzy.FuzzyChoice((False, True))
    boot_order = fuzzy.FuzzyChoice(SERVER_BOOT_ORDERS)
    host = fuzzy.FuzzyInteger(1, 8000000000)
    timezone = factory.Faker('timezone')
    account = factory.SubFactory(AccountFactory)

    plan = factory.SubFactory(PlanFactory)
    core_number = factory.LazyAttribute(make_core_number)
    memory_amount = factory.LazyAttribute(make_memory_amount)


class StorageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'upcloud.Storage'
        django_get_or_create = (
        )

    title = factory.Faker('user_name')
    access = fuzzy.FuzzyChoice(STORAGE_ACCESS)
    type = fuzzy.FuzzyChoice(STORAGE_TYPES)
    tier = fuzzy.FuzzyChoice(STORAGE_TIERS)
    size = fuzzy.FuzzyInteger(10, 1024)
    part_of_plan = fuzzy.FuzzyChoice((False, True))
    zone = factory.SubFactory(ZoneFactory)
    backup_rule_interval = fuzzy.FuzzyChoice(BACKUP_RULE_INTERVALS)
    backup_rule_time = factory.Faker('time', pattern='%H%M')
    backup_rule_retention = fuzzy.FuzzyInteger(1, 1095)
    account = factory.SubFactory(AccountFactory)


def make_ip_family(ip):
    if not ip.address:
        ip.address = fake.ipv4()
    family = 'IPv%d' % ipaddress.ip_address(ip.address).version
    return family


def make_ip_access(ip):
    access = 'public'
    if not ip.address:
        if ip.family == 'ipv6':
            ip.address = fake.ipv6()
        else:
            ip.address = fake.ipv4()
    for prefix in ('10.', '172.16', '192.168'):
        if ip.address.startswith(prefix):
            access = 'private'
    return access


class IpAddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'upcloud.IpAddress'

    address = factory.Faker('ipv4')
    family = factory.LazyAttribute(make_ip_family)
    access = factory.LazyAttribute(make_ip_access)
    part_of_plan = fuzzy.FuzzyChoice((False, True))
    ptr_record = factory.Faker('domain_name')
    server = factory.SubFactory(ServerFactory)


class FirewallRuleFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'upcloud.FirewallRule'

    server = factory.SubFactory(ServerFactory)
    action = fuzzy.FuzzyChoice(FIREWALL_RULE_ACTIONS)
    comment = factory.Faker('sentence')

    direction = fuzzy.FuzzyChoice(FIREWALL_RULE_DIRECTIONS)
    # family = factory.LazyAttribute(make_ip_family)
    protocol = fuzzy.FuzzyChoice(FIREWALL_RULE_PROTOCOLS)
    icmp_type = fuzzy.FuzzyInteger(0, 255)
    position = fuzzy.FuzzyInteger(1, 1000)
