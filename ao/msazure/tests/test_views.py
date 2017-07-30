import json
from django.test import TestCase
from faker import Faker
from ao.msazure import factories
from ao.msazure import models

faker = Faker()


class VirtualMachineViewPutTest(TestCase):
    def test_put(self):
        subscription_uuid = faker.uuid4()
        resource_group_name = faker.word()
        vm_name = 'myvm1'
        url = '/subscriptions/%s/resourceGroups/%s/providers/Microsoft.Compute/virtualMachines/%s' % (
            subscription_uuid,
            resource_group_name,
            vm_name,
        )
        with open('ao/msazure/tests/fixtures/create_vm.json') as fd:
            data = fd.read()
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, 200)
        vm = models.VirtualMachine.objects.filter(name=vm_name).first()
        self.assertIsNotNone(vm)
        self.assertEqual(str(vm.resource_group.subscription.uuid), subscription_uuid)
        self.assertEqual(vm.resource_group.name, resource_group_name)
        self.assertEqual(vm.name, vm_name)


class VirtualMachineViewGetTest(TestCase):
    def test_get(self):
        vm = factories.VirtualMachineFactory()
        url = vm.get_model_view_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, vm.model_view)

    def test_not_found(self):
        vm = factories.VirtualMachineFactory()
        base_url = vm.get_model_view_url()
        # Bad subscription
        url = base_url.replace(vm.resource_group.subscription.uuid, faker.uuid4())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Bad resource group
        url = base_url.replace(vm.resource_group.name, 'bar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Bad VM name
        url = base_url.replace(vm.name, 'ham')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class VirtualMachineViewDeleteTest(TestCase):
    def test_delete(self):
        vm = factories.VirtualMachineFactory()
        url = vm.get_model_view_url()
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 202)
        exists = models.VirtualMachine.objects.filter(id=vm.id).exists()
        self.assertFalse(exists)

    def test_not_found(self):
        vm = factories.VirtualMachineFactory()
        base_url = vm.get_model_view_url()
        # Bad subscription
        url = base_url.replace(vm.resource_group.subscription.uuid, faker.uuid4())
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        # Bad resource group
        url = base_url.replace(vm.resource_group.name, 'bar')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        # Bad VM name
        url = base_url.replace(vm.name, 'ham')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)
        # Nothin has been deleted
        exists = models.VirtualMachine.objects.filter(id=vm.id).exists()
        self.assertTrue(exists)


class VirtualMachineDeleteViewTest(TestCase):
    def test_get(self):
        vm = factories.VirtualMachineFactory()
        url = vm.get_model_view_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, vm.model_view)

    def test_not_found(self):
        vm = factories.VirtualMachineFactory()
        base_url = vm.get_model_view_url()
        # Bad subscription
        url = base_url.replace(vm.resource_group.subscription.uuid, faker.uuid4())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Bad resource group
        url = base_url.replace(vm.resource_group.name, 'bar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Bad VM name
        url = base_url.replace(vm.name, 'ham')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class VirtualMachineGetInstanceViewViewTest(TestCase):
    def test_get(self):
        vm = factories.VirtualMachineFactory()
        url = vm.get_instance_view_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, vm.instance_view)

    def test_not_found(self):
        vm = factories.VirtualMachineFactory()
        base_url = vm.get_instance_view_url()
        # Bad subscription
        url = base_url.replace(vm.resource_group.subscription.uuid, faker.uuid4())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Bad resource group
        url = base_url.replace(vm.resource_group.name, 'bar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Bad VM name
        url = base_url.replace(vm.name, 'ham')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)


class VirtualMachineListView(TestCase):
    def test_get(self):
        resource_group_name = faker.word()
        vms = factories.VirtualMachineFactory.create_batch(3, resource_group__name=resource_group_name)
        url = vms[0].get_list_url()
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        content = json.loads(response.content)
        for dbvm, vm in zip(vms, content['value']):
            self.assertEqual(dbvm.model_view, vm)

    def test_not_found(self):
        vms = factories.VirtualMachineFactory.create_batch(3)
        base_url = vms[0].get_list_url()
        # Bad subscription
        url = base_url.replace(vms[0].resource_group.subscription.uuid, faker.uuid4())
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
        # Bad resource group
        url = base_url.replace(vms[0].resource_group.name, 'bar')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)
