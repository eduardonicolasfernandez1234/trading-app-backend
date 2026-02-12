from rest_framework import serializers

from assets.models import Asset
from assets.serializers import AssetSerializer
from core.serializers.base_model_serializer import BaseModelSerializer
from signals.models import TradingSignal
from signals.serializers import TradingSignalSerializer
from trades.models import Trade, TradeAccount
from trades.serializers.trade_account_serializer import TradeAccountSerializer


class TradeSerializer(BaseModelSerializer):
    """
    Serializer para el trade lógico (contenedor de aperturas y cierres).
    """

    status_display = serializers.CharField(
        source='get_status_display',
        read_only=True
    )

    # --- FK WRITE ---
    trade_account_id = serializers.PrimaryKeyRelatedField(
        queryset=TradeAccount.objects.all(),
        write_only=True,
        source='trade_account'
    )

    asset_id = serializers.PrimaryKeyRelatedField(
        queryset=Asset.objects.all(),
        write_only=True,
        source='asset'
    )

    trading_signal_id = serializers.PrimaryKeyRelatedField(
        queryset=TradingSignal.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
        source='trading_signal'
    )

    # --- FK READ ---
    trade_account = TradeAccountSerializer(read_only=True)
    asset = AssetSerializer(read_only=True)
    trading_signal = TradingSignalSerializer(read_only=True)

    class Meta:
        model = Trade
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
