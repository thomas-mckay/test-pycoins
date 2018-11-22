from rest_framework import serializers
from rest_framework.reverse import reverse

from pycoins.models import Alert, Symbol


class SymbolSerializer(serializers.ModelSerializer):
    class Meta:
        model = Symbol
        fields = (
            'name',
            'code',
            'symbol',
            'type',
        )


class AlertSerializer(serializers.ModelSerializer):
    detail_url = serializers.SerializerMethodField(read_only=True)
    coin_obj = SymbolSerializer(read_only=True, source='coin')
    currency_obj = SymbolSerializer(read_only=True, source='currency')

    class Meta:
        model = Alert
        fields = (
            'id',
            'coin',
            'coin_obj',
            'currency',
            'currency_obj',
            'trigger_type',
            'amount',
            'evolution',
            'evolution_period',
            'message_interval',
            'activated',
            'detail_url',
        )

    def get_detail_url(self, obj):
        return reverse('api:alert-detail', kwargs={'user_pk': obj.user_id, 'pk': obj.id})

    def create(self, validated_data):
        validated_data['user'] = self.context['user']
        return super(AlertSerializer, self).create(validated_data)
