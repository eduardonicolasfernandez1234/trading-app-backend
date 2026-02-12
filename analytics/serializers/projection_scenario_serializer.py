from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserSerializer
from analytics.models import ProjectionScenario
from core.serializers.base_model_serializer import BaseModelSerializer
from signals.models import SignalSource
from signals.serializers import SignalSourceSerializer


class ProjectionScenarioSerializer(BaseModelSerializer):
    """
    Serializer para escenarios de proyección y simulación futura.
    """

    # --- FK WRITE ---
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='user'
    )

    signal_source_id = serializers.PrimaryKeyRelatedField(
        queryset=SignalSource.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
        source='signal_source'
    )

    # --- FK READ ---
    user = UserSerializer(read_only=True)
    signal_source = SignalSourceSerializer(read_only=True)

    class Meta:
        model = ProjectionScenario
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
