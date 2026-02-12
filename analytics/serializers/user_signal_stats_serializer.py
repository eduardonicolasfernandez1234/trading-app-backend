from rest_framework import serializers

from accounts.models import User
from accounts.serializers import UserSerializer
from analytics.models import UserSignalStats
from core.serializers.base_model_serializer import BaseModelSerializer
from signals.models import SignalSource, SignalProvider
from signals.serializers import SignalSourceSerializer, SignalProviderSerializer


class UserSignalStatsSerializer(BaseModelSerializer):
    """
    Serializer para estadísticas de señales por usuario.
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

    signal_provider_id = serializers.PrimaryKeyRelatedField(
        queryset=SignalProvider.objects.all(),
        write_only=True,
        required=False,
        allow_null=True,
        source='signal_provider'
    )

    # --- FK READ ---
    user = UserSerializer(read_only=True)
    signal_source = SignalSourceSerializer(read_only=True)
    signal_provider = SignalProviderSerializer(read_only=True)

    class Meta:
        model = UserSignalStats
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
