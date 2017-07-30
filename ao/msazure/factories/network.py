import factory
from factory import Faker, fuzzy
from ao.msazure.factories.common import ResourceGroupFactory
from ..models import network as models

__all__ = [
    'LoadBalancerFactory',
    'InboundNatRuleFactory',
    'BackendAddressPool',
    'PublicIpFactory',
    'VirtualNetworkFactory',
    'SubNetworkFactory',
    'NetworkInterfaceFactory',
    'NetworkSecurityGroupFactory',

    'PRIVATE_IP_ALLOCATION_METHODS',
]

PRIVATE_IP_ALLOCATION_METHODS = [i for i, j in models.PRIVATE_IP_ALLOCATION_METHODS]


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

    class Meta:
        model = 'msazure.PublicIp'


class VirtualNetworkFactory(factory.django.DjangoModelFactory):
    name = Faker('word')
    resource_group = factory.SubFactory(ResourceGroupFactory)

    class Meta:
        model = 'msazure.VirtualNetwork'


class SubNetworkFactory(factory.django.DjangoModelFactory):
    name = Faker('word')
    virtual_network = factory.SubFactory(VirtualNetworkFactory)

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
