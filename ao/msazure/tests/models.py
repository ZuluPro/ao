class IpConfigurationData(dict):
    def __init__(self, resource_group, name, subnet, private_ip, private_ip_allocation_method, public_ip, load_balancer, backend_address_pool, inbound_nat_rule, *args, **kwargs):
        super(IpConfigurationData, self).__init__(*args, **kwargs)
        self.resource_group = resource_group
        self.load_balancer = load_balancer
        self.update({
            'properties': {},
            'name': name,
        })
        self['properties']['subnet'] = {
            'id': subnet.id_
        }
        self['properties']['publicIPAddress'] = {
            'id': public_ip.id_
        }
        self['properties']['loadBalancerBackendAddressPools'] = [{
            'id': backend_address_pool.id_
        }]
        self['properties']['loadBalancerInboundNatRules'] = [{
            'id': inbound_nat_rule.id_
        }]
        self['properties'].update({
            'privateIPAddress': private_ip,
            'privateIPAllocationMethod': private_ip_allocation_method,
            'privateIPAddressVersion': 'IPv4',
        })


class CreateNetworkInterfaceData(dict):
    def __init__(self, resource_group, network_security_group, ip_configuration, enable_ip_forwarding, *args, **kwargs):
        super(CreateNetworkInterfaceData, self).__init__(*args, **kwargs)
        self.resource_group = resource_group
        self.network_security_group = network_security_group
        self['properties'] = {
            'enableIPForwarding': enable_ip_forwarding,
        }
        self['properties']['networkSecurityGroup'] = {
            'id': network_security_group.id_,
        }
        self['properties']['ipConfigurations'] = [ip_configuration]
        self['properties']['dnsSettings'] = {
            "dnsServers": [
                "10.0.0.4",
                "10.0.0.5",
            ],
            "internalDnsNameLabel": "IdnsVm1"
        }
