from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from ao.upcloud import factories


class PriceViewTest(APITestCase):
    url = reverse('upcloud:price')

    def test_get(self):
        zone = factories.ZoneFactory()
        response = self.client.get(self.url)
        self.assertIn('prices', response.data)
        self.assertIn('zone', response.data['prices'])
