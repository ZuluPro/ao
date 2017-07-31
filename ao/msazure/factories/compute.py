import factory
from factory import Faker, fuzzy
from ao.msazure.factories.common import ResourceGroupFactory
from ao.msazure.factories.network import NetworkInterfaceFactory
from ao.msazure.factories.storage import StorageAccountFactory
from ..models import compute as models

__all__ = [
    'AvaibilitySetFactory',
    'DiskFactory',
    'ImagePublisherFactory',
    'ImageOfferFactory',
    'ImageSkuFactory',
    'ImageVersion',
    'VirtualMachineFactory',
]

LOCATIONS = [i for i, j in models.common.LOCATIONS]
DISK_CACHING_MODES = [i for i, j in models.DISK_CACHING_MODES]
DISK_CREATE_OPTIONS = [i for i, j in models.DISK_CREATE_OPTIONS]


class AvaibilitySetFactory(factory.django.DjangoModelFactory):
    resource_group = factory.SubFactory(ResourceGroupFactory)
    name = Faker('word')

    class Meta:
        model = 'msazure.AvaibilitySet'
        django_get_or_create = ('resource_group', 'name',)


class DiskFactory(factory.django.DjangoModelFactory):
    resource_group = factory.SubFactory(ResourceGroupFactory)
    storage_account = factory.SubFactory(StorageAccountFactory, resource_group=factory.SelfAttribute('..resource_group'))
    location = fuzzy.FuzzyChoice(LOCATIONS)
    name = Faker('word')
    caching = fuzzy.FuzzyChoice(DISK_CACHING_MODES)
    create_option = fuzzy.FuzzyChoice(DISK_CREATE_OPTIONS)

    class Meta:
        model = 'msazure.Disk'


class ImagePublisherFactory(factory.django.DjangoModelFactory):
    name = Faker('word')
    location = fuzzy.FuzzyChoice(LOCATIONS)

    class Meta:
        model = 'msazure.ImagePublisher'


class ImageOfferFactory(factory.django.DjangoModelFactory):
    name = Faker('word')
    publisher = factory.SubFactory(ImagePublisherFactory)

    class Meta:
        model = 'msazure.ImageOffer'


class ImageSkuFactory(factory.django.DjangoModelFactory):
    name = Faker('word')
    offer = factory.SubFactory(ImageOfferFactory)

    class Meta:
        model = 'msazure.ImageSku'


class ImageVersion(factory.django.DjangoModelFactory):
    name = Faker('word')
    sku = factory.SubFactory(ImageSkuFactory)

    class Meta:
        model = 'msazure.ImageVersion'


class VirtualMachineFactory(factory.django.DjangoModelFactory):
    name = Faker('word')
    vm_id = Faker('word')
    location = fuzzy.FuzzyChoice(LOCATIONS)
    resource_group = factory.SubFactory(ResourceGroupFactory)
    avaibility_set = factory.SubFactory(AvaibilitySetFactory, resource_group=factory.SelfAttribute('..resource_group'))
    image = factory.SubFactory(ImageVersion, sku__offer__publisher__location=factory.SelfAttribute('.....location'))
    os_disk = factory.SubFactory(DiskFactory, resource_group=factory.SelfAttribute('..resource_group'))
    network_interface = factory.SubFactory(NetworkInterfaceFactory, resource_group=factory.SelfAttribute('..resource_group'))

    class Meta:
        model = 'msazure.VirtualMachine'

    @factory.post_generation
    def groups(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            for disk in extracted:
                self.data_disks.add(disk)
