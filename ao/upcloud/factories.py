import random
import ipaddress
import faker
import factory
from factory import fuzzy
from ao.upcloud import models

fake = faker.Faker()


class AccountFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'upcloud.Account'

    credits = fuzzy.FuzzyInteger(1, 10**4)
    username = factory.Faker('user_name')
    password = factory.Faker('password')


class ZoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'upcloud.Zone'

    description = factory.Faker('city')
    id = factory.LazyAttribute(lambda a: fake.slug(a.description))


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
NIC_MODELS = [i for i, j in models.NIC_MODELS]
class ServerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'upcloud.Server'

    title = factory.Faker('name')
    hostname = factory.Faker('domain_name')
    licence = 0
    state = fuzzy.FuzzyChoice(SERVER_STATES)
    zone = factory.SubFactory(ZoneFactory)
    firewall = fuzzy.FuzzyChoice((False, True))
    state = fuzzy.FuzzyChoice(SERVER_BOOT_ORDERS)
    host = fuzzy.FuzzyInteger(1, 8000000000)
    nic_model = fuzzy.FuzzyChoice(NIC_MODELS)
    timezone = factory.Faker('timezone')
    account = factory.SubFactory(AccountFactory)

    plan = factory.SubFactory(PlanFactory)
    core_number = factory.LazyAttribute(make_core_number)
    memory_amount = factory.LazyAttribute(make_memory_amount)


class StorageFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'upcloud.Storage'

    title = factory.Faker('user_name')
    access = fuzzy.FuzzyChoice(models.STORAGE_ACCESS)
    type = fuzzy.FuzzyChoice(models.STORAGE_TYPES)
    tier = fuzzy.FuzzyChoice(models.STORAGE_TIERS)
    size = fuzzy.FuzzyInteger(10, 1024)
    part_of_plan = fuzzy.FuzzyChoice((False, True))
    zone = factory.SubFactory(ZoneFactory)
    backup_rule_interval = fuzzy.FuzzyChoice(models.BACKUP_RULE_INTERVALS)
    backup_rule_time = factory.Faker('time', pattern='%H%M')
    backup_rule_retention = fuzzy.FuzzyInteger(1, 1095)
    account = factory.SubFactory(AccountFactory)


def make_ip_family(ip):
    if not ip.address:
        ip.address = fake.ipv4()
    family = 'ipv%d' % ipaddress.ip_address(ip.address).version
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
