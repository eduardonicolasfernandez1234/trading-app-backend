from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserSerializer
from analytics.models import AnalyticsSnapshot
from core.serializers.base_model_serializer import BaseModelSerializer


class AnalyticsSnapshotSerializer(BaseModelSerializer):
    """
    Serializer para snapshots históricos de métricas de trading.
    """

    snapshot_type_display = serializers.CharField(
        source='get_snapshot_type_display',
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
        model = AnalyticsSnapshot
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
