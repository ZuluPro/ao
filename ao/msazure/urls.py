from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'subscriptions/(?P<subscription_id>[^/]+)/resourceGroups/(?P<resource_group>[^/]+)/providers/Microsoft.Compute/virtualMachines$', views.VirtualMachineListView.as_view(), name='virtual-machine-list'),
    url(r'subscriptions/(?P<subscription_id>[^/]+)/resourceGroups/(?P<resource_group>[^/]+)/providers/Microsoft.Compute/virtualMachines/(?P<vm_name>[^/]+)$', views.VirtualMachineView.as_view(), name='virtual-machine-get'),
    url(r'subscriptions/(?P<subscription_id>[^/]+)/resourceGroups/(?P<resource_group>[^/]+)/providers/Microsoft.Compute/virtualMachines/(?P<vm_name>[^/]+)/InstanceView$', views.VirtualMachineGetInstanceViewView.as_view(), name='virtual-machine-get-instance-view'),
]
