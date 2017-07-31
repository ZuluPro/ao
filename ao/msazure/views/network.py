import json
from django.views.generic import View
from django.http import JsonResponse, Http404
from .. import models, factories

__all__ = [
    'PublicIpView',
    'NetworkInterfaceView',
    'SubNetworkView',
]


class PublicIpView(View):
    """
    See https://docs.microsoft.com/en-us/rest/api/network/virtualnetwork/create-or-update-a-public-ip-address
    """
    def get(self, request, subscription_id, resource_group, ip_name):
        try:
            ip = models.PublicIp.objects.get(resource_group__subscription__uuid=subscription_id,
                                             resource_group__name=resource_group,
                                             name=ip_name)
        except models.PublicIp.DoesNotExist:
            raise Http404()
        data = ip.detail_view
        # TODO: Add instance view option
        return JsonResponse(data)

    def put(self, request, subscription_id, resource_group, ip_name):
        data = json.loads(request.body)
        ip = factories.PublicIpFactory(
            name=ip_name,
            resource_group__name=resource_group,
            resource_group__subscription__uuid=subscription_id,
            location=data['location'],
            # tags=json.dumps(data['tags']),
            allocation_method=data['properties']['publicIPAllocationMethod'],
            ip_version=data['properties']['publicIPAddressVersion'],
            domain_name_label=data['properties']['dnsSettings']['domainNameLabel'],
            reverse_fqdn=data['properties']['dnsSettings']['reverseFqdn'],
        )
        data = ip.detail_view
        return JsonResponse(data)


class SubNetworkView(View):
    """
    See https://docs.microsoft.com/en-us/rest/api/network/virtualnetwork/get-information-about-a-subnet
    """
    def get(self, request, subscription_id, resource_group, net_name, subnet_name):
        try:
            nic = models.SubNetwork.objects.get(virtual_network__resource_group__subscription__uuid=subscription_id,
                                                virtual_network__resource_group__name=resource_group,
                                                virtual_network__name=net_name,
                                                name=subnet_name)
        except models.SubNetwork.DoesNotExist:
            raise Http404()
        data = nic.detail_view
        # TODO: Add instance view option
        return JsonResponse(data)


class NetworkInterfaceView(View):
    """
    See https://docs.microsoft.com/en-us/rest/api/network/virtualnetwork/create-or-update-a-network-interface-card
    """
    def get(self, request, subscription_id, resource_group, nic_name):
        try:
            nic = models.NetworkInterface.objects.get(resource_group__subscription__uuid=subscription_id,
                                                      resource_group__name=resource_group,
                                                      name=nic_name)
        except models.NetworkInterface.DoesNotExist:
            raise Http404()
        data = nic.detail_view
        # TODO: Add instance view option
        return JsonResponse(data)

    def put(self, request, subscription_id, resource_group, nic_name):
        data = json.loads(request.body)
        nic = factories.NetworkInterfaceFactory(
            name=nic_name,
            resource_group__name=resource_group,
            resource_group__subscription__uuid=subscription_id,
            location=data['location'],
            # tags=json.dumps(data['tags']),
            security_group__name=data['properties']['networkSecurityGroup']['id'].split('/')[-1],
            security_group__resource_group__name=resource_group,
            security_group__resource_group__subscription__uuid=subscription_id,
            enable_ip_forwarding=data['properties']['enableIPForwarding'],

        )
        data = nic.detail_view
        return JsonResponse(data)
