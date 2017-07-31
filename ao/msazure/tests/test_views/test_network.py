import json
from django.test import TestCase
from faker import Faker
from ao.msazure import factories
from ao.msazure import models
from ao.msazure.tests import factories as test_factories

faker = Faker()


class PublicIpPutViewTest(TestCase):
    def test_put(self):
        subscription_uuid = faker.uuid4()
        resource_group_name = faker.word()
        ip_name = faker.word()
        url = '/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Network/publicIPAddresses/%s' % (
            subscription_uuid,
            resource_group_name,
            ip_name,
        )
        data = json.dumps(test_factories.PublicIpDataFactory())
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 200)
        ip = models.PublicIp.objects.filter(name=ip_name).first()
        self.assertIsNotNone(ip)
        self.assertEqual(str(ip.resource_group.subscription.uuid), subscription_uuid)
        self.assertEqual(ip.resource_group.name, resource_group_name)
        self.assertEqual(ip.name, ip_name)


class PublicIpGetViewTest(TestCase):
    def test_get(self):
        ip = factories.PublicIpFactory()
        url = ip.get_detail_view_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, ip.detail_view)

    def test_not_found(self):
        ip = factories.PublicIpFactory()
        base_url = ip.get_detail_view_url()
        # Bad subscription
        url = base_url.replace(ip.resource_group.subscription.uuid, faker.uuid4())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Bad resource group
        url = base_url.replace(ip.resource_group.name, 'foo')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Bad IP name
        url = base_url.replace(ip.name, 'ham')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class SubNetworkViewTest(TestCase):
    def test_get(self):
        subnet = factories.SubNetworkFactory()
        url = subnet.get_detail_view_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, subnet.detail_view)

    def test_not_found(self):
        subnet = factories.SubNetworkFactory()
        base_url = subnet.get_detail_view_url()
        # Bad subscription
        url = base_url.replace(subnet.virtual_network.resource_group.subscription.uuid, faker.uuid4())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Bad resource group
        url = base_url.replace(subnet.virtual_network.resource_group.name, 'foo')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Bad network
        url = base_url.replace(subnet.virtual_network.name, 'bar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Bad VM name
        url = base_url.replace(subnet.name, 'ham')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


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
