import uuid
from django.db import models

__all__ = [
    'Subscription',
    'ResourceGroup',
]

LOCATIONS = (
    ('eastus', 'eastus'),
    ('westus', 'westus'),
    ('northus', 'northus'),
)


class Subscription(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4)


class ResourceGroup(models.Model):
    subscription = models.ForeignKey(Subscription)
    name = models.CharField(max_length=100)
