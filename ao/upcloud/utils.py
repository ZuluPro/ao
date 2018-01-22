import pytz
from django.db.models import aggregates
from . import models


def make_prices(account):
    data = {'prices': {'zone': []}}
    zones = models.Zone.objects.all()
    for index, zone in enumerate(zones):
        data['prices']['zone'].append({'name': zone.id})
        storages = zone.storage_set.filter(account=account)
        backup_amount = storages.aggregate(amount=aggregates.Sum('size'))['amount']
        hdd_amount = zone.storage_set.aggregate(amount=aggregates.Sum('size'))['amount']
        maxiops_amount = zone.storage_set.aggregate(amount=aggregates.Sum('size'))['amount']
        data['prices']['zone'][index].update({
            "firewall": {
                "amount": 0, # zone.firewall_set.count(),
                "price": zone.firewall_price,
            },
            "io_request_backup": {
                "amount": zone.io_request_backup,
                "price": zone.io_request_backup_price,
            },
            "io_request_hdd": {
                "amount": zone.io_request_hdd,
                "price": zone.io_request_hdd_price,
            },
            "io_request_maxiops": {
                "amount": zone.io_request_maxiops,
                "price": zone.io_request_maxiops_price,
            },
            "ipv4_address": {
                "amount": 0, # ipv4_count
                "price": zone.ipv4_address_price,
            },
            "ipv6_address": {
                "amount": 0, # ipv6_count
                "price": zone.ipv6_address_price,
            },
            "public_ipv4_bandwidth_in": {
                "amount": zone.public_ipv4_bandwidth_in,
                "price": zone.public_ipv4_bandwidth_in_price,
            },
            "public_ipv4_bandwidth_out": {
                "amount": zone.public_ipv4_bandwidth_out,
                "price": zone.public_ipv4_bandwidth_out_price,
            },
            "public_ipv6_bandwidth_in": {
                "amount": zone.public_ipv6_bandwidth_in,
                "price": zone.public_ipv6_bandwidth_in_price,
            },
            "public_ipv6_bandwidth_out": {
                "amount": zone.public_ipv6_bandwidth_out,
                "price": zone.public_ipv6_bandwidth_out_price,
            },
            "server_core": {
                "amount": 0, # servers_cores
                "price": zone.server_core_price,
            },
            "server_memory": {
                "amount": 0, # servers_memory
                "price": zone.server_memory_price,
            },
            "storage_backup": {
                "amount": backup_amount,
                "price": zone.storage_backup_price,
            },
            "storage_hdd": {
                "amount": hdd_amount,
                "price": zone.storage_hdd_price,
            },
            "storage_maxiops": {
                "amount": maxiops_amount,
                "price": zone.storage_maxiops_price,
            },
        })
        for plan in models.Plan.objects.all():
            plan_key = 'server_plan_%s' % plan.id
            field_name = 'plan_%scpu_price' % plan.core_number
            amount = plan.server_set.count()
            if hasattr(zone, field_name):
                price = getattr(zone, field_name)
            else:
                price = (plan.core_number*memory_amount)/.9
            data['prices']['zone'][index].append({
                "amount": amount,
                "price": price,
            })
    return data


def make_timezones():
    data = {'timezones': {'timezone': pytz.all_timezones,}}
    return data
