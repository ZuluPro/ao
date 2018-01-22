from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from ao.upcloud import factories


class ZoneViewTest(APITestCase):
    url = reverse('upcloud:zone')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertIn('zones', response.data)
        self.assertIn('zone', response.data['zones'])
