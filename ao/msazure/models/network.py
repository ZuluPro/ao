import uuid
from django.db import models
from django.urls import reverse_lazy as reverse
from . import common

__all__ = [
    'NetworkSecurityGroup',
    'VirtualNetwork',
    'SubNetwork',
    'PublicIp',
    'LoadBalancer',
    'BackendAddressPool',
    'InboundNatRule',
    'NetworkInterface',
    'IpConfiguration',
]

IP_ALLOCATION_METHODS = (
  ('Static', 'Static'),
  ('Dynamic', 'Dynamic'),
)
IP_VERSIONS = (
    ('ipv4', 'IPv4'),
    ('ipv6', 'IPv6'),
)


class NetworkSecurityGroup(models.Model):
    name = models.CharField(max_length=100)
    resource_group = models.ForeignKey('msazure.ResourceGroup')

    type = 'Microsoft.Network/networkSecurityGroups'

    @property
    def id_(self):
        temp = '/subscriptions/%s/resourceGroups/%s/providers/%s/%s'
        return temp % (
            self.resource_group.subscription.uuid,
            self.resource_group.name,
            self.type,
            self.name,
        )


class VirtualNetwork(models.Model):
    name = models.CharField(max_length=100)
    resource_group = models.ForeignKey('msazure.ResourceGroup')

    type = 'Microsoft.Network/virtualNetworks'

    @property
    def id_(self):
        temp = '/subscriptions/%s/resourceGroups/%s/providers/%s/%s'
        return temp % (
            self.resource_group.subscription.uuid,
            self.resource_group.name,
            self.type,
            self.name,
        )


class RouteTable(models.Model):
    name = models.CharField(max_length=100)
    resource_group = models.ForeignKey('msazure.ResourceGroup')

    type = 'Microsoft.Network/routeTables'

    @property
    def id_(self):
        temp = '/subscriptions/%s/resourceGroups/%s/providers/%s/%s'
        return temp % (
            self.resource_group.subscription.uuid,
            self.resource_group.name,
            self.type,
            self.name,
        )


class SubNetwork(models.Model):
    name = models.CharField(max_length=100)
    virtual_network = models.ForeignKey(VirtualNetwork)
    etag = models.CharField(max_length=100)
    provisioning_state = models.CharField(max_length=20)
    address_prefix = models.CharField(max_length=18)
    security_group = models.ForeignKey(NetworkSecurityGroup)
    route_table = models.ForeignKey(RouteTable)

    type = 'Microsoft.Network/networkInterfaces'

    @property
    def id_(self):
        temp = '/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/virtualNetworks/%s/subnets/%s'
        return temp % (
            self.virtual_network.resource_group.subscription.uuid,
            self.virtual_network.resource_group.name,
            self.virtual_network.name,
            self.name,
        )

    def get_detail_view_url(self):
        return reverse('subnetwork', kwargs={
            'subscription_id': self.virtual_network.resource_group.subscription.uuid,
            'resource_group': self.virtual_network.resource_group.name,
            'net_name': self.virtual_network.name,
            'subnet_name': self.name,
        })

    @property
    def detail_view(self):
        data = {
            'name': self.name,
            'id': self.id_,
            'etag': self.etag,
            'properties': {
                'provisioningState': self.provisioning_state,
                'addressPrefix': self.address_prefix,
                'networkSecurityGroup': {'id': self.security_group.id_},
                'routeTable': {'id': self.route_table.id_},
                'ipConfigurations': [{'id': ipconf.id_} for ipconf in self.ipconfiguration_set.all()]
            }
        }
        return data


    @property
    def id_(self):
        temp = '/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/virtualNetworks/%s/subnets/%s'
        return temp % (
            self.virtual_network.resource_group.subscription.uuid,
            self.virtual_network.resource_group.name,
            self.virtual_network.name,
            self.name,
        )


class PublicIp(models.Model):
    name = models.CharField(max_length=100)
    ip = models.GenericIPAddressField()
    resource_group = models.ForeignKey('msazure.ResourceGroup')
    etag = models.CharField(max_length=100)
    uuid = models.UUIDField(default=uuid.uuid4)
    provisioning_state = models.CharField(max_length=20)
    location = models.CharField(max_length=20, choices=common.LOCATIONS)
    allocation_method = models.CharField(max_length=10, choices=IP_ALLOCATION_METHODS)
    ip_version = models.CharField(max_length=4, choices=IP_VERSIONS)
    idle_timeout = models.PositiveSmallIntegerField(default=30)
    domain_name_label = models.CharField(max_length=100)
    reverse_fqdn = models.CharField(max_length=100)

    type = 'Microsoft.Network/publicIPAddresses'

    @property
    def id_(self):
        temp = '/subscriptions/%s/resourceGroups/%s/providers/%s/%s'
        return temp % (
            self.resource_group.subscription.uuid,
            self.resource_group.name,
            self.type,
            self.name,
        )

    def get_detail_view_url(self):
        return reverse('public-ip', kwargs={
            'subscription_id': self.resource_group.subscription.uuid,
            'resource_group': self.resource_group.name,
            'ip_name': self.name,
        })

    @property
    def detail_view(self):
        data = {
            'location': self.location,
            'etag': 'W/"%s"' % self.etag,
            'tags': {},
            'properties': {
                'resourceGuid': str(self.uuid),
                'provisioningState': self.provisioning_state,
                'ipAddress': self.ip,
                'publicIPAllocationMethod': self.allocation_method,
                'publicIPAddressVersion': self.ip_version,
                'idleTimeoutInMinutes': self.idle_timeout,
                'dnsSettings': {
                    'domainNameLabel': self.domain_name_label,
                    'reverseFqdn': self.reverse_fqdn,
                }
            }
        }
        if self.ipconfiguration_set.exists():
            ipconf = self.ipconfiguration_set.first()
            data['properties']['ipConfiguration'] = {
                'id': ipconf.id_,
            }
        return data


class LoadBalancer(models.Model):
    name = models.CharField(max_length=100)
    resource_group = models.ForeignKey('msazure.ResourceGroup')


class BackendAddressPool(models.Model):
    name = models.CharField(max_length=100)
    load_balancer = models.ForeignKey(LoadBalancer)

    @property
    def id_(self):
        temp = '/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/loadBalancers/%s/backendAddressPools/%s'
        return temp % (
            self.load_balancer.resource_group.subscription.uuid,
            self.load_balancer.resource_group.name,
            self.load_balancer.name,
            self.name,
        )


class InboundNatRule(models.Model):
    name = models.CharField(max_length=100)
    load_balancer = models.ForeignKey(LoadBalancer)

    @property
    def id_(self):
        temp = '/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/loadBalancers/%s/inboundNatRules/%s'
        return temp % (
            self.load_balancer.resource_group.subscription.uuid,
            self.load_balancer.resource_group.name,
            self.load_balancer.name,
            self.name,
        )


class NetworkInterface(models.Model):
    resource_group = models.ForeignKey('msazure.ResourceGroup')
    location = models.CharField(max_length=20, choices=common.LOCATIONS)
    name = models.CharField(max_length=100)
    security_group = models.ForeignKey(NetworkSecurityGroup)
    enable_ip_forwarding = models.BooleanField()
    etag = models.CharField(max_length=100)
    provisioning_state = models.CharField(max_length=30)
    mac_address = models.CharField(max_length=17)
    # primary = models.BooleanField()

    type = 'Microsoft.Network/networkInterfaces'

    @property
    def id_(self):
        temp = '/subscriptions/%s/resourceGroups/%s/providers/%s/%s'
        return temp % (
            self.resource_group.subscription.uuid,
            self.resource_group.name,
            self.type,
            self.name,
        )

    def get_detail_view_url(self):
        return reverse('network-interface', kwargs={
            'subscription_id': self.resource_group.subscription.uuid,
            'resource_group': self.resource_group.name,
            'nic_name': self.name,
        })

    @property
    def detail_view(self):
        data = {
            'name': self.name,
            'id': self.id_,
            'location': self.location,
            'etag': 'W/"%s"' % self.etag,
            'type': self.type,
            'properties': {
                'resourcesubscriptionId': self.resource_group.subscription.uuid,
                'provisioningState': self.provisioning_state,
            },
            'macAddress': self.mac_address,
            'networkSecurityGroup': {
                'id': self.security_group.id_,
            },
            'dnsSettings': {
            }
        }
        if self.virtualmachine_set.exists():
            vm = self.virtualmachine_set.first()
            data['virtualMachine'] = vm.id_
            data['dnsSettings'].update({
                'dnsServers': ["10.0.0.4", "10.0.0.5"],
                "appliedDnsServers": ["1.0.0.1", "2.0.0.2", "3.0.0.3"],
                "internalDnsNameLabel": vm.computer_name,
                "internalFqdn": "%s.a2ftlxfjn2iezihj3udx1wfn4d.hx.internal.cloudapp.net" % vm.name,
                "internalDomainNameSuffix": "a2ftlxfjn2iezihj3udx1wfn4d.hx.internal.cloudapp.net",
            })
        if self.ipconfiguration_set.exists():
            data['ipConfigurations'] = []
            for ipconf in self.ipconfiguration_set.all():
                ipconf_data = {
                    "name": ipconf.name,
                    "id": ipconf.id_,
                    "etag": ipconf.etag,
                    "properties": {
                        "provisioningState": ipconf.provisioning_state,
                        "subnet": {
                            'id': ipconf.subnet.id_
                        },
                        "privateIPAddress": ipconf.private_ip,
                        "privateIPAllocationMethod": ipconf.private_ip_allocation_method,
                        "privateIPAddressVersion": "IPv4",
                        "publicIPAddress": {
                            "id": ipconf.public_ip.id_
                        },
                        "loadBalancerBackendAddressPools": {
                            "id": ipconf.backend_address_pool.id_
                        },
                    }
                }
                if ipconf.inbound_nat_rules.exists():
                    ipconf_data['loadBalancerInboundNatRules'] = []
                    for rule in ipconf.inbound_nat_rules.all():
                        ipconf_data['loadBalancerInboundNatRules'].append({
                            'id': rule.id_
                        })
        return data


class IpConfiguration(models.Model):
    name = models.CharField(max_length=100)
    network_inteface = models.ForeignKey(NetworkInterface)
    subnetwork = models.ForeignKey(SubNetwork)
    provisioning_state = models.CharField(max_length=30)
    etag = models.CharField(max_length=100)
    private_ip = models.GenericIPAddressField()
    private_ip_allocation_method = models.CharField(max_length=10, choices=IP_ALLOCATION_METHODS)
    public_ip = models.ForeignKey(PublicIp)
    backend_address_pool = models.ForeignKey(BackendAddressPool)
    inbound_nat_rules = models.ManyToManyField(InboundNatRule)

    @property
    def id_(self):
        temp = '/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/networkInterfaces/%s/ipConfigurations/%s'
        return temp % (
            self.network_inteface.resource_group.subscription.uuid,
            self.network_inteface.resource_group.name,
            self.network_inteface.name,
            self.name,
        )
