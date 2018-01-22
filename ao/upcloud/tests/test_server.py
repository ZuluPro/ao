from mock import patch
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from ao.upcloud import factories
from ao.core import fields


class ListServerTest(APITestCase):
    url = reverse('upcloud:server-list')

    def test_list_empty(self):
        response = self.client.get(self.url)
        data = {'servers': {'server': []}}
        self.assertEqual(data, response.data)

    def test_list(self):
        servers = {str(o.uuid): o for o in factories.ServerFactory.create_batch(3)}
        response = self.client.get(self.url)
        self.assertIn('servers', response.data)
        self.assertIn('server', response.data['servers'])
        for server_data in response.data['servers']['server']:
            server = servers[server_data['uuid']]
            expected = {
	        'uuid': str(server.uuid),
                'firewall': fields.OnOffField().to_representation(server.firewall),
                'timezone': server.timezone,
                'password_delivery': 'none',
                'title': server.title,
                'hostname': server.hostname,
                'licence': 0,
                'core_number': server.core_number,
                'memory_amount': server.memory_amount,
                'state': server.state,
                'boot_order': 'cdrom,disk',
                'host': 4281901271,
                'nic_model': 'e1000',
                'plan': server.plan.name,
                'zone': server.zone.id,
            }

    def test_list_level_0(self):
        account = factories.AccountFactory()
        servers = {str(o.uuid): o for o in factories.ServerFactory.create_batch(3, account=account)}
        servers.update({str(o.uuid): o for o in factories.ServerFactory.create_batch(3)})
        response = self.client.get(self.url)
        self.assertEqual(len(response.data['servers']['server']), 6)

    @patch('ao.upcloud.views.ServerViewSet.access_level', 1)
    def test_list_level_1(self):
        account = factories.AccountFactory()
        servers = {str(o.uuid): o for o in factories.ServerFactory.create_batch(3, account=account)}
        servers.update({str(o.uuid): o for o in factories.ServerFactory.create_batch(3)})
        response = self.client.get(self.url, HTTP_AUTHORIZATION='Basic ' + account.api_key.decode())
        self.assertEqual(len(response.data['servers']['server']), 3)
