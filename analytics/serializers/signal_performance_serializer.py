from rest_framework import serializers

from analytics.models import SignalPerformance
from core.serializers.base_model_serializer import BaseModelSerializer
from signals.models import TradingSignal
from signals.serializers import TradingSignalSerializer


class SignalPerformanceSerializer(BaseModelSerializer):
    """
    Serializer para el desempeño teórico de una señal.
    """

    # --- FK WRITE ---
    trading_signal_id = serializers.PrimaryKeyRelatedField(
        queryset=TradingSignal.objects.all(),
        write_only=True,
        source='trading_signal'
    )

    # --- FK READ ---
    trading_signal = TradingSignalSerializer(read_only=True)

    class Meta:
        model = SignalPerformance
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
