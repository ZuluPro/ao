from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from ao.upcloud import factories


class PlanViewTest(APITestCase):
    url = reverse('upcloud:plan')

    def test_get(self):
        response = self.client.get(self.url)
        self.assertIn('plans', response.data)
        self.assertIn('plan', response.data['plans'])
