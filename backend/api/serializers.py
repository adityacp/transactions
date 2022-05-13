# Django Imports
from rest_framework import serializers


class UserSerializer(serializers.Serializer):
    username = serializers.CharField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField()
    last_login = serializers.DateTimeField()
    date_joined = serializers.DateTimeField()

    def __init__(self, *args, **kwargs):
        fields = kwargs.get('context', {}).get("fields", None)
        exclude = kwargs.get('context', {}).get("exclude", None)
        super(UserSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name)


class AccountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    user = UserSerializer(context={"fields": ["first_name", "last_name"]})
    balance = serializers.IntegerField()

    def __init__(self, *args, **kwargs):
        fields = kwargs.get('context', {}).get("fields", None)
        exclude = kwargs.get('context', {}).get("exclude", None)
        super(AccountSerializer, self).__init__(*args, **kwargs)
        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)
        if exclude is not None:
            for field_name in exclude:
                self.fields.pop(field_name)


class TransactionSerializer(serializers.Serializer):
    transaction_id = serializers.UUIDField()
    status = serializers.CharField()
    type = serializers.CharField()
    reason = serializers.CharField()
    transaction_from = AccountSerializer(context={"fields": ["id", "user"]})
    transaction_to = AccountSerializer(context={"fields": ["id", "user"]})
    amount = serializers.IntegerField()
    created_on = serializers.DateTimeField()
    updated_on = serializers.DateTimeField()
