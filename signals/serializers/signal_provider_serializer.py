from rest_framework import serializers

from core.serializers.base_model_serializer import BaseModelSerializer
from signals.models import SignalProvider, SignalSource
from signals.serializers.signal_source_serializer import SignalSourceSerializer


class SignalProviderSerializer(BaseModelSerializer):
    signal_source_id = serializers.PrimaryKeyRelatedField(
        queryset=SignalSource.objects.all(),
        write_only=True,
        source='signal_source'
    )
    signal_source = SignalSourceSerializer(read_only=True)

    class Meta:
        model = SignalProvider
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
