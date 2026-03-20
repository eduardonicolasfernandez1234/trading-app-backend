from rest_framework import serializers

from core.serializers.base_model_serializer import BaseModelSerializer
from .models import TelegramAccount


class TelegramAccountSerializer(BaseModelSerializer):
    is_authenticated = serializers.SerializerMethodField()
    is_running = serializers.SerializerMethodField()

    def get_is_authenticated(self, obj):
        return obj.is_authenticated

    def get_is_running(self, obj):
        return obj.is_running

    class Meta(BaseModelSerializer.Meta):
        model = TelegramAccount
        fields = '__all__'
        extra_kwargs = {
            'api_hash': {'write_only': True},
            'phone_code_hash': {'read_only': True},
            'session_name': {'read_only': True},
            'pid': {'read_only': True},
            'awaiting_2fa': {'read_only': True},
        }
