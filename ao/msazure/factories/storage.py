import factory
from factory import Faker, fuzzy
from ao.msazure.factories.common import ResourceGroupFactory
from ..models import storage as models

__all__ = [
    'StorageAccountFactory',
]

STORAGE_ACCOUNT_SKUS = [i for i, j in models.STORAGE_ACCOUNT_SKUS]
STORAGE_ACCOUNT_KINDS = [i for i, j in models.STORAGE_ACCOUNT_KINDS]
STORAGE_ACCOUNT_ACCESS_TIER = [i for i, j in models.STORAGE_ACCOUNT_ACCESS_TIER]


class StorageAccountFactory(factory.django.DjangoModelFactory):
    resource_group = factory.SubFactory(ResourceGroupFactory)
    name = Faker('word')
    sku = fuzzy.FuzzyChoice(STORAGE_ACCOUNT_SKUS)
    kind = fuzzy.FuzzyChoice(STORAGE_ACCOUNT_KINDS)
    access_tier = fuzzy.FuzzyChoice(STORAGE_ACCOUNT_ACCESS_TIER)

    class Meta:
        model = 'msazure.StorageAccount'
