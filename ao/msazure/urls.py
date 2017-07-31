from django.conf.urls import url
from . import views

urlpatterns = [
    # Network
    url(r'subscriptions/(?P<subscription_id>[^/]+)/resourceGroups/(?P<resource_group>[^/]+)/providers/Microsoft.Network/publicIPAddresses/(?P<ip_name>[^/]+)$', views.PublicIpView.as_view(), name='public-ip'),
    url(r'subscriptions/(?P<subscription_id>[^/]+)/resourceGroups/(?P<resource_group>[^/]+)/providers/Microsoft.Network/VirtualNetworks/(?P<net_name>[^/]+)/subnets/(?P<subnet_name>[^/]+)$', views.SubNetworkView.as_view(), name='subnetwork'),
    url(r'subscriptions/(?P<subscription_id>[^/]+)/resourceGroups/(?P<resource_group>[^/]+)/providers/Microsoft.Network/networkInterfaces/(?P<nic_name>[^/]+)$', views.NetworkInterfaceView.as_view(), name='network-interface'),
    # Virtual machines
    url(r'subscriptions/(?P<subscription_id>[^/]+)/resourceGroups/(?P<resource_group>[^/]+)/providers/Microsoft.Compute/virtualMachines$', views.VirtualMachineListView.as_view(), name='virtual-machine-list'),
    url(r'subscriptions/(?P<subscription_id>[^/]+)/resourceGroups/(?P<resource_group>[^/]+)/providers/Microsoft.Compute/virtualMachines/(?P<vm_name>[^/]+)$', views.VirtualMachineView.as_view(), name='virtual-machine-get'),
    url(r'subscriptions/(?P<subscription_id>[^/]+)/resourceGroups/(?P<resource_group>[^/]+)/providers/Microsoft.Compute/virtualMachines/(?P<vm_name>[^/]+)/InstanceView$', views.VirtualMachineGetInstanceViewView.as_view(), name='virtual-machine-get-instance-view'),
]
