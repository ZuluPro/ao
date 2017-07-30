from django.test import TestCase
from ao.msazure import validators


class ValidateDiskNameTest(TestCase):
    def validate(self):
        # Alpha
        validators.validate_disk_name('foo')
        # Int
        validators.validate_disk_name('123')
        # _
        validators.validate_disk_name('bar_456')

    def not_validate(self):
        # Too long
        with self.assertRaises(validators.ValidationError):
            validators.validate_disk_name('foobarham'*10)
        # Space
        with self.assertRaises(validators.ValidationError):
            validators.validate_disk_name('foo ')
        # dash
        with self.assertRaises(validators.ValidationError):
            validators.validate_disk_name('bar-3')
        # Weird
        with self.assertRaises(validators.ValidationError):
            validators.validate_disk_name('h@m')
