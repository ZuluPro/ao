import factory
from factory import Faker, fuzzy
from . import models

LOCATIONS = [i for i, j in models.LOCATIONS]
DISK_CACHING_MODES = [i for i, j in models.DISK_CACHING_MODES]
DISK_CREATE_OPTIONS = [i for i, j in models.DISK_CREATE_OPTIONS]
STORAGE_ACCOUNT_SKUS = [i for i, j in models.STORAGE_ACCOUNT_SKUS]
STORAGE_ACCOUNT_KINDS = [i for i, j in models.STORAGE_ACCOUNT_KINDS]
STORAGE_ACCOUNT_ACCESS_TIER = [i for i, j in models.STORAGE_ACCOUNT_ACCESS_TIER]


class SubscriptionFactory(factory.django.DjangoModelFactory):
    uuid = Faker('uuid4')

    class Meta:
        model = 'msazure.Subscription'
        django_get_or_create = ('uuid',)


class ResourceGroupFactory(factory.django.DjangoModelFactory):
    subscription = factory.SubFactory(SubscriptionFactory)
    name = Faker('word')

    class Meta:
        model = 'msazure.ResourceGroup'
        django_get_or_create = ('subscription', 'name',)


class AvaibilitySetFactory(factory.django.DjangoModelFactory):
    resource_group = factory.SubFactory(ResourceGroupFactory)
    name = Faker('word')

    class Meta:
        model = 'msazure.AvaibilitySet'
        django_get_or_create = ('resource_group', 'name',)


class StorageAccountFactory(factory.django.DjangoModelFactory):
    resource_group = factory.SubFactory(ResourceGroupFactory)
    name = Faker('word')
    sku = fuzzy.FuzzyChoice(STORAGE_ACCOUNT_SKUS)
    kind = fuzzy.FuzzyChoice(STORAGE_ACCOUNT_KINDS)
    access_tier = fuzzy.FuzzyChoice(STORAGE_ACCOUNT_ACCESS_TIER)

    class Meta:
        model = 'msazure.StorageAccount'


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


class NetworkInterfaceFactory(factory.django.DjangoModelFactory):
    resource_group = factory.SubFactory(ResourceGroupFactory)

    class Meta:
        model = 'msazure.NetworkInterface'


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
