from mock import patch
from rest_framework.test import APITestCase
from rest_framework.reverse import reverse
from ao.upcloud import factories
from ao.core import fields


class ListStorageTest(APITestCase):
    url = reverse('upcloud:storage-list')

    def test_list_empty(self):
        response = self.client.get(self.url)
        data = {'storages': {'storage': []}}
        self.assertEqual(data, response.data)

    def test_list(self):
        storage = {str(o.uuid): o for o in factories.StorageFactory.create_batch(3)}
        response = self.client.get(self.url)
        self.assertIn('storages', response.data)
        self.assertIn('storage', response.data['storages'])


class ListStoragePublicTest(APITestCase):
    url = reverse('upcloud:storage-public')

    def test_list(self):
        factories.StorageFactory()
        storage = {
            str(s.uuid): s for s in factories.StorageFactory\
                .create_batch(3, account=None)
        }
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('storages', data)
        self.assertIn('storage', data['storages'])
        self.assertEqual(3, len(data['storages']['storage']))


class ListStoragePrivateTest(APITestCase):
    url = reverse('upcloud:storage-private')

    def test_list(self):
        account = factories.AccountFactory()
        factories.StorageFactory(account=None)
        storage = {
            str(s.uuid): s for s in factories.StorageFactory\
                .create_batch(3, account=account)
        }
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('storages', data)
        self.assertIn('storage', data['storages'])
        self.assertEqual(0, len(data['storages']['storage']))


class ListStorageNormalTest(APITestCase):
    url = reverse('upcloud:storage-normal')

    def test_list(self):
        account = factories.AccountFactory()
        factories.StorageFactory(account=None)
        storage = {
            str(s.uuid): s for s in factories.StorageFactory\
                .create_batch(3, account=account, type='normal')
        }
        response = self.client.get(self.url, HTTP_AUTHORIZATION='Basic ' + account.api_key.decode())
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('storages', data)
        self.assertIn('storage', data['storages'])
        self.assertEqual(3, len(data['storages']['storage']))


class ListStorageBackupTest(APITestCase):
    url = reverse('upcloud:storage-backup')

    def test_list(self):
        account = factories.AccountFactory()
        factories.StorageFactory(account=None)
        storage = {
            str(s.uuid): s for s in factories.StorageFactory\
                .create_batch(3, account=account, type='backup')
        }
        response = self.client.get(self.url, HTTP_AUTHORIZATION='Basic ' + account.api_key.decode())
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('storages', data)
        self.assertIn('storage', data['storages'])
        self.assertEqual(3, len(data['storages']['storage']))


class ListStorageCdromTest(APITestCase):
    url = reverse('upcloud:storage-cdrom')

    def test_list(self):
        account = factories.AccountFactory()
        factories.StorageFactory(account=None)
        storage = {
            str(s.uuid): s for s in factories.StorageFactory\
                .create_batch(3, account=account, type='cdrom')
        }
        response = self.client.get(self.url, HTTP_AUTHORIZATION='Basic ' + account.api_key.decode())
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('storages', data)
        self.assertIn('storage', data['storages'])
        self.assertEqual(3, len(data['storages']['storage']))


class ListStorageTemplateTest(APITestCase):
    url = reverse('upcloud:storage-template')

    def test_list(self):
        account = factories.AccountFactory()
        factories.StorageFactory(account=None)
        storage = {
            str(s.uuid): s for s in factories.StorageFactory\
                .create_batch(3, account=account, type='template')
        }
        response = self.client.get(self.url, HTTP_AUTHORIZATION='Basic ' + account.api_key.decode())
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('storages', data)
        self.assertIn('storage', data['storages'])
        self.assertEqual(3, len(data['storages']['storage']))


class ListStorageFavoriteTest(APITestCase):
    url = reverse('upcloud:storage-favorite')

    def test_list(self):
        account = factories.AccountFactory()
        factories.StorageFactory(account=None)
        storage = {
            str(s.uuid): s for s in factories.StorageFactory\
                .create_batch(3, account=account, favorite=True)
        }
        response = self.client.get(self.url, HTTP_AUTHORIZATION='Basic ' + account.api_key.decode())
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn('storages', data)
        self.assertIn('storage', data['storages'])
        self.assertEqual(3, len(data['storages']['storage']))
