# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-31 02:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AvaibilitySet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='BackendAddressPool',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Disk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(choices=[(b'eastus', b'eastus'), (b'westus', b'westus'), (b'northus', b'northus')], max_length=20)),
                ('os_type', models.CharField(blank=True, max_length=20, null=True)),
                ('vhd_uri', models.CharField(max_length=255)),
                ('caching', models.CharField(choices=[(b'None', b'None'), (b'ReadOnly', b'ReadOnly'), (b'ReadWrite', b'ReadWrite')], max_length=10)),
                ('create_option', models.CharField(choices=[(b'fromImage', b'fromImage'), (b'attach', b'attach')], max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='ImageOffer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ImagePublisher',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(choices=[(b'eastus', b'eastus'), (b'westus', b'westus'), (b'northus', b'northus')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ImageSku',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.ImageOffer')),
            ],
        ),
        migrations.CreateModel(
            name='ImageVersion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sku', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.ImageSku')),
            ],
        ),
        migrations.CreateModel(
            name='InboundNatRule',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='IpConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('provisioning_state', models.CharField(max_length=30)),
                ('etag', models.CharField(max_length=100)),
                ('private_ip', models.GenericIPAddressField()),
                ('private_ip_allocation_method', models.CharField(choices=[(b'Static', b'Static'), (b'Dynamic', b'Dynamic')], max_length=10)),
                ('backend_address_pool', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.BackendAddressPool')),
                ('inbound_nat_rules', models.ManyToManyField(to='msazure.InboundNatRule')),
            ],
        ),
        migrations.CreateModel(
            name='LoadBalancer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='NetworkInterface',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(choices=[(b'eastus', b'eastus'), (b'westus', b'westus'), (b'northus', b'northus')], max_length=20)),
                ('name', models.CharField(max_length=100)),
                ('enable_ip_forwarding', models.BooleanField()),
                ('etag', models.CharField(max_length=100)),
                ('provisioning_state', models.CharField(max_length=30)),
                ('mac_address', models.CharField(max_length=17)),
            ],
        ),
        migrations.CreateModel(
            name='NetworkSecurityGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='PublicIp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ip', models.GenericIPAddressField()),
                ('etag', models.CharField(max_length=100)),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
                ('provisioning_state', models.CharField(max_length=20)),
                ('location', models.CharField(choices=[(b'eastus', b'eastus'), (b'westus', b'westus'), (b'northus', b'northus')], max_length=20)),
                ('allocation_method', models.CharField(choices=[(b'Static', b'Static'), (b'Dynamic', b'Dynamic')], max_length=10)),
                ('ip_version', models.CharField(choices=[(b'ipv4', b'IPv4'), (b'ipv6', b'IPv6')], max_length=4)),
                ('idle_timeout', models.PositiveSmallIntegerField(default=30)),
                ('domain_name_label', models.CharField(max_length=100)),
                ('reverse_fqdn', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ResourceGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='RouteTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('resource_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.ResourceGroup')),
            ],
        ),
        migrations.CreateModel(
            name='StorageAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('sku', models.CharField(choices=[(b'Standard_LRS', b'Standard_LRS'), (b'Standard_GRS', b'Standard_GRS'), (b'Premium_LRS', b'Premium_LRS')], max_length=30)),
                ('kind', models.CharField(choices=[(b'Storage', b'Storage'), (b'BlobStorage', b'BlobStorage')], max_length=30)),
                ('access_tier', models.CharField(choices=[(b'Cool', b'Cool'), (b'Hot', b'Hot')], max_length=30)),
                ('tags', models.TextField(default=b'{}', max_length=2000)),
                ('resource_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.ResourceGroup')),
            ],
        ),
        migrations.CreateModel(
            name='SubNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('etag', models.CharField(max_length=100)),
                ('provisioning_state', models.CharField(max_length=20)),
                ('address_prefix', models.CharField(max_length=18)),
                ('route_table', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.RouteTable')),
                ('security_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.NetworkSecurityGroup')),
            ],
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4)),
            ],
        ),
        migrations.CreateModel(
            name='VirtualMachine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vm_id', models.CharField(max_length=128)),
                ('name', models.CharField(max_length=100)),
                ('location', models.CharField(choices=[(b'eastus', b'eastus'), (b'westus', b'westus'), (b'northus', b'northus')], max_length=20)),
                ('tags', models.TextField(default=b'{}', max_length=2000)),
                ('provisioning_state', models.CharField(max_length=20)),
                ('vm_size', models.CharField(max_length=30)),
                ('computer_name', models.CharField(max_length=100)),
                ('admin_username', models.CharField(max_length=100)),
                ('admin_password', models.CharField(max_length=100)),
                ('custom_data', models.TextField(max_length=100)),
                ('avaibility_set', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.AvaibilitySet')),
                ('data_disks', models.ManyToManyField(to='msazure.Disk')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.ImageVersion')),
                ('network_interface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.NetworkInterface')),
                ('os_disk', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='root_on_instances', to='msazure.Disk')),
                ('resource_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.ResourceGroup')),
            ],
        ),
        migrations.CreateModel(
            name='VirtualNetwork',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('resource_group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.ResourceGroup')),
            ],
        ),
        migrations.AddField(
            model_name='subnetwork',
            name='virtual_network',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.VirtualNetwork'),
        ),
        migrations.AddField(
            model_name='resourcegroup',
            name='subscription',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.Subscription'),
        ),
        migrations.AddField(
            model_name='publicip',
            name='resource_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.ResourceGroup'),
        ),
        migrations.AddField(
            model_name='networksecuritygroup',
            name='resource_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.ResourceGroup'),
        ),
        migrations.AddField(
            model_name='networkinterface',
            name='resource_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.ResourceGroup'),
        ),
        migrations.AddField(
            model_name='networkinterface',
            name='security_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.NetworkSecurityGroup'),
        ),
        migrations.AddField(
            model_name='loadbalancer',
            name='resource_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.ResourceGroup'),
        ),
        migrations.AddField(
            model_name='ipconfiguration',
            name='network_inteface',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.NetworkInterface'),
        ),
        migrations.AddField(
            model_name='ipconfiguration',
            name='public_ip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.PublicIp'),
        ),
        migrations.AddField(
            model_name='ipconfiguration',
            name='subnetwork',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.SubNetwork'),
        ),
        migrations.AddField(
            model_name='inboundnatrule',
            name='load_balancer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.LoadBalancer'),
        ),
        migrations.AddField(
            model_name='imageoffer',
            name='publisher',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.ImagePublisher'),
        ),
        migrations.AddField(
            model_name='disk',
            name='resource_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.ResourceGroup'),
        ),
        migrations.AddField(
            model_name='disk',
            name='storage_account',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.StorageAccount'),
        ),
        migrations.AddField(
            model_name='backendaddresspool',
            name='load_balancer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.LoadBalancer'),
        ),
        migrations.AddField(
            model_name='avaibilityset',
            name='resource_group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='msazure.ResourceGroup'),
        ),
        migrations.AlterUniqueTogether(
            name='virtualmachine',
            unique_together=set([('name', 'resource_group')]),
        ),
    ]
