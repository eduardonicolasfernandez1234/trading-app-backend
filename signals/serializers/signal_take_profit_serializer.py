from rest_framework import serializers

from core.serializers.base_model_serializer import BaseModelSerializer
from signals.models import SignalTakeProfit
from signals.models import TradingSignal


class SignalTakeProfitSerializer(BaseModelSerializer):
    trading_signal_id = serializers.PrimaryKeyRelatedField(
        queryset=TradingSignal.objects.all(),
        write_only=True,
        source='trading_signal'
    )
    trading_signal = serializers.SerializerMethodField()

    class Meta:
        model = SignalTakeProfit
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields

    def get_trading_signal(self, obj):
        from signals.serializers import TradingSignalSerializer
        return TradingSignalSerializer(obj)
