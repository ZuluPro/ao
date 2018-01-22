from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from ao.upcloud import factories


class AccountViewTest(APITestCase):
    url = reverse('upcloud:account')

    def test_list_empty(self):
        response = self.client.get(self.url)
        self.assertIn('account', response.data)
        self.assertIn('credits', response.data['account'])
        self.assertIn('username', response.data['account'])
