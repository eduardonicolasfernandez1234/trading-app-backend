from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserSerializer
from analytics.models import AnalyticsRun
from core.serializers.base_model_serializer import BaseModelSerializer


class AnalyticsRunSerializer(BaseModelSerializer):
    """
    Serializer para ejecuciones de procesos analíticos.
    """

    analysis_type_display = serializers.CharField(
        source='get_analysis_type_display',
        read_only=True
    )

    # --- FK WRITE ---
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='user'
    )

    # --- FK READ ---
    user = UserSerializer(read_only=True)

    class Meta:
        model = AnalyticsRun
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
