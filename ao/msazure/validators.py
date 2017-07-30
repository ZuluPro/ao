import re
from django.core.exceptions import ValidationError

DISK_NAME_REG = re.compile(r'^[A-z0-9_]{1,80}$')


def validate_disk_name(value):
    if DISK_NAME_REG.match(value) is None:
        raise ValidationError(
            "Disk name supports %s" % DISK_NAME_REG.pattern,
            params={'value': value},
        )
