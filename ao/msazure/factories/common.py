import factory
from factory import Faker

__all__ = [
    'SubscriptionFactory',
    'ResourceGroupFactory',
]


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
