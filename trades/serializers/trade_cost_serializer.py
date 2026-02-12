from rest_framework import serializers

from core.serializers.base_model_serializer import BaseModelSerializer
from trades.models import TradeCost, Trade, TradeClose


class TradeCostSerializer(BaseModelSerializer):
    """
    Serializer para costos asociados a trades o cierres.
    """

    cost_type_display = serializers.CharField(
        source='get_cost_type_display',
        read_only=True
    )

    # --- FK WRITE ---
    trade_id = serializers.PrimaryKeyRelatedField(
        queryset=Trade.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
        source='trade'
    )

    trade_close_id = serializers.PrimaryKeyRelatedField(
        queryset=TradeClose.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
        source='trade_close'
    )

    class Meta:
        model = TradeCost
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
