from rest_framework import serializers

from core.serializers.base_model_serializer import BaseModelSerializer
from trades.models import TradeCloseResult, TradeClose


class TradeCloseResultSerializer(BaseModelSerializer):
    """
    Serializer para resultados financieros de un cierre de trade.
    """

    # --- FK WRITE ---
    trade_close_id = serializers.PrimaryKeyRelatedField(
        queryset=TradeClose.objects.all(),
        write_only=True,
        source='trade_close'
    )

    class Meta:
        model = TradeCloseResult
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
