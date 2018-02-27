from rest_framework import fields


class EmptyIfNoneField(fields.Field):
    def __init__(self, parent, *args, **kwargs):
        super(EmptyIfNoneField, self).__init__(*args, **kwargs) 
        self.parent = parent(*args, **kwargs)

    def to_representation(self, obj):
        import ipdb; ipdb.set_trace()
        if obj is None:
            return ''
        return self.parent.to_representation(obj)

    def to_internal_value(self, data):
        return self.parent.to_internal_value(data)


class BoolField(fields.Field):
    def to_representation(self, obj):
        return self.TRUE if obj else self.FALSE

    def to_internal_value(self, data):
        if data == self.TRUE:
            return True
        elif data == self.FALSE:
            return False
        return


class OnOffField(BoolField):
    TRUE = 'on'
    FALSE = 'off'


class YesNoField(BoolField):
    TRUE = 'yes'
    FALSE = 'no'


class SshKeyField(fields.CharField):
    # TODO: Validation
    pass

    def create(self, *args, **kwargs):
        pass


class SshKeyListField(fields.ListField):
    child = SshKeyField()

    def create(self, *args, **kwargs):
        pass
