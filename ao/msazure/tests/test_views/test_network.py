import json
from django.test import TestCase
from faker import Faker
from ao.msazure import factories
from ao.msazure import models
from ao.msazure.tests import factories as test_factories

faker = Faker()


class NetworkInterfaceViewPut(TestCase):
    def test_put(self):
        subscription_uuid = faker.uuid4()
        resource_group_name = faker.word()
        nic_name = 'nicfoo'
        url = '/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/networkInterfaces/%s' % (
            subscription_uuid,
            resource_group_name,
            nic_name,
        )
        data = json.dumps(test_factories.CreateNetworkInterfaceDataFactory())
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 200)
        nic = models.NetworkInterface.objects.filter(name=nic_name).first()
        self.assertIsNotNone(nic)
        self.assertEqual(str(nic.resource_group.subscription.uuid), subscription_uuid)
        self.assertEqual(nic.resource_group.name, resource_group_name)
        self.assertEqual(nic.name, nic_name)


class NetworkInterfaceViewGet(TestCase):
    def test_get(self):
        nic = factories.NetworkInterfaceFactory()
        url = nic.get_detail_view_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, nic.detail_view)

    def test_not_found(self):
        nic = factories.NetworkInterfaceFactory()
        base_url = nic.get_detail_view_url()
        # Bad subscription
        url = base_url.replace(nic.resource_group.subscription.uuid, faker.uuid4())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Bad resource group
        url = base_url.replace(nic.resource_group.name, 'bar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Bad VM name
        url = base_url.replace(nic.name, 'ham')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
