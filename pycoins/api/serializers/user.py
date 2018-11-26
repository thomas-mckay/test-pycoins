from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    id = serializers.HyperlinkedIdentityField(view_name='api:user-detail')
    password = serializers.CharField(required=False, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'first_name', 'last_name', 'email')

    def validate_password(self, value):
        return make_password(value)
