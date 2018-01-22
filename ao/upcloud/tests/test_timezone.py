from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from ao.upcloud import factories


class TimezoneViewTest(APITestCase):
    url = reverse('upcloud:timezone')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertIn('timezones', response.data)
        self.assertIn('timezone', response.data['timezones'])
