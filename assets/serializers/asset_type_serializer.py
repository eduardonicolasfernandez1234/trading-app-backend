from assets.models import AssetType
from core.serializers.base_model_serializer import BaseModelSerializer


class AssetTypeSerializer(BaseModelSerializer):
    """
    Serializer para tipos de activos (Forex, Crypto, Commodities, etc.).
    """

    class Meta:
        model = AssetType
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
