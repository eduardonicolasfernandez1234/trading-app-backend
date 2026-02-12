from rest_framework import serializers

from core.serializers.base_model_serializer import BaseModelSerializer
from signals.models import SignalContext
from signals.models import TradingSignal


class SignalContextSerializer(BaseModelSerializer):
    market_condition_display = serializers.CharField(
        source='get_market_condition_display',
        read_only=True
    )

    volatility_level_display = serializers.CharField(
        source='get_volatility_level_display',
        read_only=True
    )

    trading_signal_id = serializers.PrimaryKeyRelatedField(
        queryset=TradingSignal.objects.all(),
        write_only=True,
        source='trading_signal'
    )
    trading_signal = serializers.SerializerMethodField()

    class Meta:
        model = SignalContext
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields

    def get_trading_signal(self, obj):
        from signals.serializers import TradingSignalSerializer
        return TradingSignalSerializer(obj)
