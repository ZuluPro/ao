import factory
from factory import Faker, fuzzy
from ao.msazure.factories.common import ResourceGroupFactory
from ..models import network as models

__all__ = [
    'LoadBalancerFactory',
    'InboundNatRuleFactory',
    'BackendAddressPool',
    'PublicIpFactory',
    'RouteTableFactory',
    'VirtualNetworkFactory',
    'SubNetworkFactory',
    'NetworkSecurityGroupFactory',
    'NetworkInterfaceFactory',
    'NetworkSecurityGroupFactory',

    'IP_ALLOCATION_METHODS',
]

LOCATIONS = [i for i, j in models.common.LOCATIONS]
IP_ALLOCATION_METHODS = [i for i, j in models.IP_ALLOCATION_METHODS]


class LoadBalancerFactory(factory.django.DjangoModelFactory):
    name = Faker('word')
    resource_group = factory.SubFactory(ResourceGroupFactory)

    class Meta:
        model = 'msazure.LoadBalancer'


class InboundNatRuleFactory(factory.django.DjangoModelFactory):
    name = Faker('word')
    load_balancer = factory.SubFactory(LoadBalancerFactory)

    class Meta:
        model = 'msazure.InboundNatRule'


class BackendAddressPool(factory.django.DjangoModelFactory):
    load_balancer = factory.SubFactory(LoadBalancerFactory)

    class Meta:
        model = 'msazure.BackendAddressPool'


class PublicIpFactory(factory.django.DjangoModelFactory):
    name = Faker('word')
    ip = Faker('ipv4')
    resource_group = factory.SubFactory(ResourceGroupFactory)
    location = fuzzy.FuzzyChoice(LOCATIONS)
    ip_version = 'ipv4'
    idle_timeout = fuzzy.FuzzyInteger(4, 30)
    domain_name_label = Faker('word')
    reverse_fqdn = Faker('domain_name')

    class Meta:
        model = 'msazure.PublicIp'


class VirtualNetworkFactory(factory.django.DjangoModelFactory):
    name = Faker('word')
    resource_group = factory.SubFactory(ResourceGroupFactory)

    class Meta:
        model = 'msazure.VirtualNetwork'


class NetworkSecurityGroupFactory(factory.django.DjangoModelFactory):
    name = Faker('word')
    resource_group = factory.SubFactory(ResourceGroupFactory)

    class Meta:
        model = 'msazure.NetworkSecurityGroup'


class RouteTableFactory(factory.django.DjangoModelFactory):
    name = Faker('word')
    resource_group = factory.SubFactory(ResourceGroupFactory)

    class Meta:
        model = 'msazure.RouteTable'


class SubNetworkFactory(factory.django.DjangoModelFactory):
    name = Faker('word')
    etag = factory.LazyFunction(lambda: 'W/"%s"' % Faker('uuid4').generate({}))
    provisioning_state = 'Succeed'
    address_prefix = Faker('ipv4', network=True)
    virtual_network = factory.SubFactory(VirtualNetworkFactory)
    security_group = factory.SubFactory(NetworkSecurityGroupFactory, resource_group=factory.SelfAttribute('..virtual_network.resource_group'))
    route_table = factory.SubFactory(RouteTableFactory, resource_group=factory.SelfAttribute('..virtual_network.resource_group'))

    class Meta:
        model = 'msazure.SubNetwork'


class NetworkSecurityGroupFactory(factory.django.DjangoModelFactory):
    name = Faker('word')
    resource_group = factory.SubFactory(ResourceGroupFactory)

    class Meta:
        model = 'msazure.NetworkSecurityGroup'


class NetworkInterfaceFactory(factory.django.DjangoModelFactory):
    resource_group = factory.SubFactory(ResourceGroupFactory)
    name = Faker('word')
    enable_ip_forwarding = fuzzy.FuzzyChoice([True, False])
    etag = factory.LazyFunction(lambda: 'W/"%s"' % Faker('uuid4').generate({}))
    provisioning_state = 'Succeed'
    mac_address = Faker('mac_address')
    security_group = factory.SubFactory(NetworkSecurityGroupFactory, resource_group=factory.SelfAttribute('..resource_group'))

    class Meta:
        model = 'msazure.NetworkInterface'
