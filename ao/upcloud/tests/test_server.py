from rest_framework.test import APITestCase
from rest_framework.reverse import reverse


class ListServerTest(APITestCase):
    url = reverse('upcloud:server-list')

    def test_list(self):
        response = self.client.get(self.url)
        data = {'servers': {'server': []}}
        self.assertEqual(data, response.data)
