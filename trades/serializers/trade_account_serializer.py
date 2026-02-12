from core.serializers.base_model_serializer import BaseModelSerializer
from trades.models import TradeAccount


class TradeAccountSerializer(BaseModelSerializer):
    """
    Serializer para cuentas de trading.
    """

    class Meta:
        model = TradeAccount
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
