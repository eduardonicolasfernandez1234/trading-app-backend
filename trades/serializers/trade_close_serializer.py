from rest_framework import serializers

from core.serializers.base_model_serializer import BaseModelSerializer
from trades.models import TradeClose, Trade


class TradeCloseSerializer(BaseModelSerializer):
    """
    Serializer para cierres parciales o totales de un trade.
    """

    close_reason_display = serializers.CharField(
        source='get_close_reason_display',
        read_only=True
    )

    # --- FK WRITE ---
    trade_id = serializers.PrimaryKeyRelatedField(
        queryset=Trade.objects.all(),
        write_only=True,
        source='trade'
    )

    class Meta:
        model = TradeClose
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
