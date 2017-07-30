import json
from django.db import models
from django.urls import reverse_lazy as reverse
from . import common

__all__ = [
    'AvaibilitySet',
    'StorageAccount',
    'Disk',
    'ImagePublisher',
    'ImageOffer',
    'ImageSku',
    'ImageVersion',
    'VirtualMachine',
]

DISK_CACHING_MODES = (
  ('None', 'None'),
  ('ReadOnly', 'ReadOnly'),
  ('ReadWrite', 'ReadWrite'),
)
DISK_CREATE_OPTIONS = (
  ('fromImage', 'fromImage'),
  ('attach', 'attach'),
)
STORAGE_ACCOUNT_SKUS = (
  ('Standard_LRS', 'Standard_LRS'),
  # ('Standard_ZRS', 'Standard_ZRS'),
  ('Standard_GRS', 'Standard_GRS'),
  # ('Standard_RAGRS', 'Standard_RAGRS'),
  ('Premium_LRS', 'Premium_LRS'),
)
STORAGE_ACCOUNT_KINDS = (
  ('Storage', 'Storage'),
  ('BlobStorage', 'BlobStorage'),
)
STORAGE_ACCOUNT_ACCESS_TIER = (
  ('Cool', 'Cool'),
  ('Hot', 'Hot'),
)


class AvaibilitySet(models.Model):
    resource_group = models.ForeignKey('msazure.ResourceGroup')
    name = models.CharField(max_length=100)

    type = 'Microsoft.Compute/availabilitySets'

    @property
    def id_(self):
        temp = '/subscriptions/%s/resourceGroups/%s/providers/%s/%s'
        return temp % (
            self.resource_group.subscription.uuid,
            self.resource_group.name,
            self.type,
            self.name,
        )


class StorageAccount(models.Model):
    resource_group = models.ForeignKey('msazure.ResourceGroup')
    name = models.CharField(max_length=100)
    sku = models.CharField(max_length=30, choices=STORAGE_ACCOUNT_SKUS)
    kind = models.CharField(max_length=30, choices=STORAGE_ACCOUNT_KINDS)
    access_tier = models.CharField(max_length=30, choices=STORAGE_ACCOUNT_ACCESS_TIER)
    tags = models.TextField(max_length=2000, default='{}')


class Disk(models.Model):
    resource_group = models.ForeignKey('msazure.ResourceGroup')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=20, choices=common.LOCATIONS)
    os_type = models.CharField(max_length=20, blank=True, null=True)
    vhd_uri = models.CharField(max_length=255)
    caching = models.CharField(max_length=10, choices=DISK_CACHING_MODES)
    create_option = models.CharField(max_length=20, choices=DISK_CREATE_OPTIONS)
    storage_account = models.ForeignKey(StorageAccount)

    type = "Microsoft.Compute/disks"

    @property
    def id_(self):
        temp = '/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Compute/disks/%s'
        return temp % (
            self.resource_group.subscription.uuid,
            self.resource_group.name,
            self.name
        )


class ImagePublisher(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, choices=common.LOCATIONS)


class ImageOffer(models.Model):
    name = models.CharField(max_length=100)
    publisher = models.ForeignKey(ImagePublisher)


class ImageSku(models.Model):
    name = models.CharField(max_length=100)
    offer = models.ForeignKey(ImageOffer)


class ImageVersion(models.Model):
    name = models.CharField(max_length=100)
    sku = models.ForeignKey(ImageSku)

    def get_id(self, subscription_uuid):
        temp = '/subscriptions/%s/providers/Microsoft.Compute/locations/%s/publishers/%s/artifactype/vmimage/offers/%s/skus/%s/versions/%s'
        return temp % (
            subscription_uuid,
            self.sku.offer.publisher.location,
            self.sku.offer.publisher.name,
            self.sku.offer.name,
            self.sku.name,
            self.name,
        )


class VirtualMachine(models.Model):
    vm_id = models.CharField(max_length=128)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=20, choices=common.LOCATIONS)
    tags = models.TextField(max_length=2000, default='{}')
    resource_group = models.ForeignKey('msazure.ResourceGroup')
    avaibility_set = models.ForeignKey(AvaibilitySet)
    provisioning_state = models.CharField(max_length=20)
    # Hardware
    vm_size = models.CharField(max_length=30)
    # Storage
    image = models.ForeignKey(ImageVersion)
    os_disk = models.ForeignKey(Disk, related_name='root_on_instances')
    data_disks = models.ManyToManyField(Disk)
    # Profile
    computer_name = models.CharField(max_length=100)
    admin_username = models.CharField(max_length=100)
    admin_password = models.CharField(max_length=100)
    custom_data = models.TextField(max_length=100)
    # Network
    network_interface = models.ForeignKey('msazure.NetworkInterface')

    type = "Microsoft.Compute/virtualMachines"

    class Meta:
        unique_together = (
            ('name', 'resource_group'),
        )

    def __str__(self):
        return self.id_

    def get_model_view_url(self):
        return reverse('virtual-machine-get', kwargs={
            'subscription_id': self.resource_group.subscription.uuid,
            'resource_group': self.resource_group.name,
            'vm_name': self.name,
        })

    def get_instance_view_url(self):
        return reverse('virtual-machine-get-instance-view', kwargs={
            'subscription_id': self.resource_group.subscription.uuid,
            'resource_group': self.resource_group.name,
            'vm_name': self.name,
        })

    def get_list_url(self):
        return reverse('virtual-machine-list', kwargs={
            'subscription_id': self.resource_group.subscription.uuid,
            'resource_group': self.resource_group.name,
        })

    @property
    def id_(self):
        temp = '/subscriptions/%s/resourceGroups/%s/providers/%s/%s'
        return temp % (
            self.resource_group.subscription.uuid,
            self.resource_group.name,
            self.type,
            self.name
        )

    @property
    def model_view(self):
        return {
          "id": self.id_,
          "vmId": self.vm_id,
          "name": self.name,
          "type": self.type,
          "location": self.location,
          "tags": json.loads(self.tags),
          "properties": {
             "licenseType": "Windows_Server",
             "availabilitySet": {
                "id": self.avaibility_set.id_,
             },
             "hardwareProfile": {
                "vmSize": self.vm_size,
             },
             "storageProfile": {
                "imageReference": {
                   "publisher": self.image.sku.offer.publisher.name,
                   "offer": self.image.sku.offer.name,
                   "sku": self.image.sku.name,
                   "version": self.image.name,
                   "id": self.image.get_id(self.resource_group.subscription.uuid),
                },
                "osDisk": {
                   "osType": self.os_disk.os_type,
                   "name": self.os_disk.name,
                   "managedDisk": {
                     "Id": self.os_disk.id_,
                     "storageAccountType": self.os_disk.storage_account.sku,
                   },
                   "vhd": {
                      "uri": self.os_disk.vhd_uri,
                   },
                   "caching": self.os_disk.caching,
                   "createOption": self.os_disk.create_option
                },
                "dataDisks": []
             },
             "osProfile": {
                "computerName": self.computer_name,
                "adminUsername": self.admin_username,
                "adminPassword": self.admin_password,
                "customData": "",
                "windowsConfiguration": {
                   "provisionVMAgent": True,
                   "winRM": {
                      "listeners": [{
                        "protocol": "https",
                        "certificateUrl": "[parameters('certificateUrl')]"
                      }]
                   },
                   "additionalUnattendContent": [{
                         "pass": "oobesystem",
                         "component": "Microsoft-Windows-Shell-Setup",
                         "settingName": "AutoLogon",
                         "content": "<XML unattend content>",
                         "enableAutomaticUpdates": True
                   }],
                   "secrets": [],
                },
                "networkProfile": {
                   "networkInterfaces": [
                      {
                         "id": self.network_interface.id_,
                      }
                   ]
                },
                "provisioningState": self.provisioning_state,
             }
          }
       }

    @property
    def instance_view(self):
        def format_disk(disk):
            return {
              "name": disk.name,
              "statuses": [
                {
                  "code": "ProvisioningState/succeeded",
                  "level": "Info",
                  "displayStatus": "Provisioning succeeded",
                  "time": "2015-04-10T12:44:10.4562812-07:00"
                }
              ]
            }
        return {
          "platformUpdateDomain": 0,
          "platformFaultDomain": 0,
          "vmAgent": {
            "vmAgentVersion": "2.5.1198.709",
            "statuses": [
              {
                "code": "ProvisioningState/succeeded",
                "level": "Info",
                "displayStatus": "Ready",
                "message": "GuestAgent is running and accepting new configurations.",
                "time": "2015-04-21T11:42:44-07:00"
              }
            ]
          },
          "disks": [format_disk(self.os_disk)] + [format_disk(d) for d in self.data_disks.all()],
          "statuses": [
            {
              "code": "ProvisioningState/succeeded",
              "level": "Info",
              "displayStatus": "Provisioning succeeded",
              "time": "2015-04-10T12:50:09.0031588-07:00"
            },
            {
              "code": "PowerState/running",
              "level": "Info",
              "displayStatus": "VM running"
            }
          ]
        }
