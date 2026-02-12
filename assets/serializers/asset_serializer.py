from rest_framework import serializers

from assets.models import Asset, AssetType
from assets.serializers.asset_type_serializer import AssetTypeSerializer
from core.serializers.base_model_serializer import BaseModelSerializer


class AssetSerializer(BaseModelSerializer):
    """
    Serializer para activos operables (XAUUSD, BTCUSDT, etc.).
    """

    # --- FK WRITE ---
    asset_type_id = serializers.PrimaryKeyRelatedField(
        queryset=AssetType.objects.all(),
        write_only=True,
        source='asset_type'
    )

    # --- FK READ ---
    asset_type = AssetTypeSerializer(read_only=True)

    class Meta:
        model = Asset
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
