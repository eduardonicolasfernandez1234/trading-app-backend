from rest_framework import serializers

from core.serializers.base_model_serializer import BaseModelSerializer
from trades.models import TradeEntry, Trade


class TradeEntrySerializer(BaseModelSerializer):
    """
    Serializer para aperturas de trade (scaling in).
    """

    entry_source_display = serializers.CharField(
        source='get_entry_source_display',
        read_only=True
    )

    # --- FK WRITE ---
    trade_id = serializers.PrimaryKeyRelatedField(
        queryset=Trade.objects.all(),
        write_only=True,
        source='trade'
    )

    class Meta:
        model = TradeEntry
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
