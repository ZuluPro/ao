from django.conf.urls import url
from . import views

urlpatterns = [
    # Network
    url(r'subscriptions/(?P<subscription_id>[^/]+)/resourceGroups/(?P<resource_group>[^/]+)/providers/Microsoft.Network/networkInterfaces/(?P<nic_name>[^/]+)$', views.NetworkInterfaceView.as_view(), name='network-interface'),
    # Virtual machines
    url(r'subscriptions/(?P<subscription_id>[^/]+)/resourceGroups/(?P<resource_group>[^/]+)/providers/Microsoft.Compute/virtualMachines$', views.VirtualMachineListView.as_view(), name='virtual-machine-list'),
    url(r'subscriptions/(?P<subscription_id>[^/]+)/resourceGroups/(?P<resource_group>[^/]+)/providers/Microsoft.Compute/virtualMachines/(?P<vm_name>[^/]+)$', views.VirtualMachineView.as_view(), name='virtual-machine-get'),
    url(r'subscriptions/(?P<subscription_id>[^/]+)/resourceGroups/(?P<resource_group>[^/]+)/providers/Microsoft.Compute/virtualMachines/(?P<vm_name>[^/]+)/InstanceView$', views.VirtualMachineGetInstanceViewView.as_view(), name='virtual-machine-get-instance-view'),
]
