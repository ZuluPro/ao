import factory
from factory import Faker, fuzzy
from ao.msazure import factories
from . import models


class IpConfigurationDataFactory(factory.Factory):
    name = Faker('word')
    resource_group = factory.SubFactory(factories.ResourceGroupFactory)
    subnet = factory.SubFactory(factories.SubNetworkFactory, virtual_network__resource_group=factory.SelfAttribute('...resource_group'))
    private_ip = Faker('ipv4')
    private_ip_allocation_method = fuzzy.FuzzyChoice(factories.PRIVATE_IP_ALLOCATION_METHODS)
    subnet = factory.SubFactory(factories.SubNetworkFactory, virtual_network__resource_group=factory.SelfAttribute('...resource_group'))
    public_ip = factory.SubFactory(factories.PublicIpFactory, resource_group=factory.SelfAttribute('..resource_group'))
    backend_address_pool = factory.SubFactory(factories.BackendAddressPool, load_balancer=factory.SelfAttribute('..load_balancer'))
    load_balancer = factory.SubFactory(factories.LoadBalancerFactory, resource_group=factory.SelfAttribute('...resource_group'))
    inbound_nat_rule = factory.SubFactory(factories.InboundNatRuleFactory, load_balancer=factory.SelfAttribute('..load_balancer'))

    class Meta:
        model = models.IpConfigurationData


class CreateNetworkInterfaceDataFactory(factory.Factory):
    location = fuzzy.FuzzyChoice(factories.compute.LOCATIONS)
    # tags = {}
    enable_ip_forwarding = fuzzy.FuzzyChoice([True, False])
    resource_group = factory.SubFactory(factories.ResourceGroupFactory)
    network_security_group = factory.SubFactory(factories.NetworkSecurityGroupFactory, resource_group=factory.SelfAttribute('..resource_group'))
    ip_configuration = factory.SubFactory(IpConfigurationDataFactory, resource_group=factory.SelfAttribute('..resource_group'))

    class Meta:
        model = models.CreateNetworkInterfaceData
