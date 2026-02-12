from rest_framework import serializers

from assets.models import AssetTradingSchedule, Asset
from assets.serializers.asset_serializer import AssetSerializer
from core.serializers.base_model_serializer import BaseModelSerializer


class AssetTradingScheduleSerializer(BaseModelSerializer):
    """
    Serializer para horarios de trading de un activo.
    """

    # --- DISPLAY ---
    day_of_week_display = serializers.SerializerMethodField(read_only=True)

    # --- FK WRITE ---
    asset_id = serializers.PrimaryKeyRelatedField(
        queryset=Asset.objects.all(),
        write_only=True,
        source='asset'
    )

    # --- FK READ ---
    asset = AssetSerializer(read_only=True)

    class Meta:
        model = AssetTradingSchedule
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields

    def get_day_of_week_display(self, obj):
        days = {
            0: 'Lunes',
            1: 'Martes',
            2: 'Miércoles',
            3: 'Jueves',
            4: 'Viernes',
            5: 'Sábado',
            6: 'Domingo',
        }
        return days.get(obj.day_of_week)
