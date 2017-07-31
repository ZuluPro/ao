from django.db import models
from django.urls import reverse_lazy as reverse
from . import common

__all__ = [
    'StorageAccount',
]

STORAGE_ACCOUNT_SKUS = (
  ('Standard_LRS', 'Standard LRS'),
  # ('Standard_ZRS', 'Standard_ZRS'),
  ('Standard_GRS', 'Standard GRS'),
  # ('Standard_RAGRS', 'Standard RAGRS'),
  ('Premium_LRS', 'Premium LRS'),
)
STORAGE_ACCOUNT_SKU_TIERS = (
  ('Standard', 'Standard'),
  ('Premium', 'Premium'),
)
STORAGE_ACCOUNT_KINDS = (
  ('Storage', 'Storage'),
  ('BlobStorage', 'BlobStorage'),
)
STORAGE_ACCOUNT_ACCESS_TIER = (
  ('Cool', 'Cool'),
  ('Hot', 'Hot'),
)


class StorageAccount(models.Model):
    resource_group = models.ForeignKey('msazure.ResourceGroup')
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=20, choices=common.LOCATIONS)
    sku = models.CharField(max_length=30, choices=STORAGE_ACCOUNT_SKUS)
    sku_tier = models.CharField(max_length=30, choices=STORAGE_ACCOUNT_SKU_TIERS)
    kind = models.CharField(max_length=30, choices=STORAGE_ACCOUNT_KINDS)
    access_tier = models.CharField(max_length=30, choices=STORAGE_ACCOUNT_ACCESS_TIER)
    tags = models.TextField(max_length=2000, default='{}')

    type = 'Microsoft.Storage/storageAccounts'

    @property
    def id_(self):
        temp = '/subscriptions/%s/resourceGroups/%s/providers/%s/%s'
        return temp % (
            self.resource_group.subscription.uuid,
            self.resource_group.name,
            self.type,
            self.name,
        )

    @property
    def detail_view(self):
        data = {
            'id': self.id_,
            'name': self.name,
            'location': self.location,
            'type': self.type,
            'properties': {},
            'sku': {
                'name': self.sku,
                'tier': self.sku_tier,
            },
            'kind': self.kind,
        }
        return data
