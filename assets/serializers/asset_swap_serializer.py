from rest_framework import serializers

from assets.models import AssetSwap, Asset
from assets.serializers.asset_serializer import AssetSerializer
from core.serializers.base_model_serializer import BaseModelSerializer


class AssetSwapSerializer(BaseModelSerializer):
    """
    Serializer para configuración de swaps de un activo.
    """

    # --- DISPLAY ---
    triple_swap_day_display = serializers.SerializerMethodField(read_only=True)

    # --- FK WRITE ---
    asset_id = serializers.PrimaryKeyRelatedField(
        queryset=Asset.objects.all(),
        write_only=True,
        source='asset'
    )

    # --- FK READ ---
    asset = AssetSerializer(read_only=True)

    class Meta:
        model = AssetSwap
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields

    def get_triple_swap_day_display(self, obj):
        days = {
            0: 'Lunes',
            1: 'Martes',
            2: 'Miércoles',
            3: 'Jueves',
            4: 'Viernes',
            5: 'Sábado',
            6: 'Domingo',
        }
        return days.get(obj.triple_swap_day)
