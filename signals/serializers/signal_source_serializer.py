from rest_framework import serializers

from core.serializers.base_model_serializer import BaseModelSerializer
from signals.models import SignalSource


class SignalSourceSerializer(BaseModelSerializer):
    platform_display = serializers.CharField(
        source='get_platform_display',
        read_only=True
    )

    signal_style_display = serializers.CharField(
        source='get_signal_style_display',
        read_only=True
    )

    risk_profile_display = serializers.CharField(
        source='get_risk_profile_display',
        read_only=True
    )

    class Meta:
        model = SignalSource
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
