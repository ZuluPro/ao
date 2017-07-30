import json
from django.views.generic import View
from django.http import JsonResponse, Http404
from . import models, factories


class VirtualMachineView(View):
    """
    See https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/virtualmachines-get
    - Model View: https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Compute/virtualMachines/{vm}?api-version={apiVersion}
    - +Instance View: https://management.azure.com/subscriptions/{subscriptionId}/resourceGroups/{resourceGroup}/providers/Microsoft.Compute/virtualMachines/{vm}?$expand=instanceView&api-version={apiVersion}
    """
    def get(self, request, subscription_id, resource_group, vm_name):
        try:
            vm = models.VirtualMachine.objects.get(resource_group__subscription__uuid=subscription_id,
                                                   resource_group__name=resource_group,
                                                   name=vm_name)
        except models.VirtualMachine.DoesNotExist:
            raise Http404()
        data = vm.model_view
        # TODO: Add instance view option
        return JsonResponse(data)

    def put(self, request, subscription_id, resource_group, vm_name):
        data = json.loads(request.body)
        vm = factories.VirtualMachineFactory(
            name=vm_name,
            resource_group__name=resource_group,
            resource_group__subscription__uuid=subscription_id,
            location=data['location'],
            tags=json.dumps(data['tags']),
            vm_size=data['properties']['hardwareProfile']['vmSize'],
            image__name=data['properties']['storageProfile']['imageReference']['version'],
            image__sku__name=data['properties']['storageProfile']['imageReference']['sku'],
            image__sku__offer__name=data['properties']['storageProfile']['imageReference']['offer'],
            image__sku__offer__publisher__name=data['properties']['storageProfile']['imageReference']['publisher'],
            os_disk__name=data['properties']['storageProfile']['osDisk']['name'],
            os_disk__vhd_uri=data['properties']['storageProfile']['osDisk']['vhd']['uri'],
            os_disk__caching=data['properties']['storageProfile']['osDisk']['caching'],
            computer_name=data['properties']['osProfile']['computerName'],
            admin_username=data['properties']['osProfile']['adminUsername'],
            admin_password=data['properties']['osProfile']['adminPassword'],
            network_interface__name=data['properties']['networkProfile']['networkInterfaces'][0]['id'].split('/')[-1],
        )
        data = vm.model_view
        return JsonResponse(data)

    def delete(self, request, subscription_id, resource_group, vm_name):
        """
        See https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/virtualmachines-delete
        """
        try:
            vm = models.VirtualMachine.objects.get(resource_group__subscription__uuid=subscription_id,
                                                   resource_group__name=resource_group,
                                                   name=vm_name)
        except models.VirtualMachine.DoesNotExist:
            raise Http404()
        # TODO: Elaborate
        vm.delete()
        return JsonResponse({}, status=202)


class VirtualMachineGetInstanceViewView(View):
    """
    See https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/virtualmachines-get
    """
    def get(self, request, subscription_id, resource_group, vm_name):
        try:
            vm = models.VirtualMachine.objects.get(resource_group__subscription__uuid=subscription_id,
                                                   resource_group__name=resource_group,
                                                   name=vm_name)
        except models.VirtualMachine.DoesNotExist:
            raise Http404()
        data = vm.instance_view
        return JsonResponse(data)


class VirtualMachineListView(View):
    """
    See https://docs.microsoft.com/en-us/rest/api/compute/virtualmachines/virtualmachines-list-resource-group
    """
    def get(self, request, subscription_id, resource_group):
        subscription_exists = models.Subscription.objects\
                .filter(uuid=subscription_id)\
                .exists()
        if not subscription_exists:
            # TODO : See real message
            raise Http404()
        group_exists = models.ResourceGroup.objects\
                .filter(subscription__uuid=subscription_id, name=resource_group)\
                .exists()
        if not group_exists:
            # TODO : See real message
            raise Http404()
        vms = models.VirtualMachine.objects\
            .filter(resource_group__name=resource_group,
                    resource_group__subscription__uuid=subscription_id)
        data = {'value': [vm.model_view for vm in vms]}
        return JsonResponse(data)
