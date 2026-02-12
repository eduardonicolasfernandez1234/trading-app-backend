from rest_framework import serializers

from assets.models import Asset
from core.serializers.base_model_serializer import BaseModelSerializer
from signals.models import SignalSource, SignalProvider
from signals.models import TradingSignal
from signals.serializers.signal_context_serializer import SignalContextSerializer
from signals.serializers.signal_provider_serializer import SignalProviderSerializer
from signals.serializers.signal_source_serializer import SignalSourceSerializer
from signals.serializers.signal_take_profit_serializer import SignalTakeProfitSerializer


class TradingSignalSerializer(BaseModelSerializer):
    # --- DISPLAY FIELDS ---
    direction_display = serializers.CharField(
        source='get_direction_display',
        read_only=True
    )

    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    execution_type_display = serializers.CharField(
        source='get_execution_type_display',
        read_only=True
    )

    confidence_level_display = serializers.CharField(
        source='get_confidence_level_display',
        read_only=True
    )

    session_display = serializers.CharField(
        source='get_session_display',
        read_only=True
    )

    # --- FK WRITE ---
    signal_source_id = serializers.PrimaryKeyRelatedField(
        queryset=SignalSource.objects.all(),
        write_only=True,
        source='signal_source'
    )

    signal_provider_id = serializers.PrimaryKeyRelatedField(
        queryset=SignalProvider.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
        source='signal_provider'
    )

    asset_id = serializers.PrimaryKeyRelatedField(
        queryset=Asset.objects.all(),
        write_only=True,
        source='asset'
    )

    # --- FK READ ---
    signal_source = SignalSourceSerializer(read_only=True)
    signal_provider = SignalProviderSerializer(read_only=True)
    asset = serializers.StringRelatedField(read_only=True)

    # --- RELATIONS ---
    take_profits = SignalTakeProfitSerializer(many=True, read_only=True)
    context = SignalContextSerializer(read_only=True)

    class Meta:
        model = TradingSignal
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
