from rest_framework import serializers

from accounts.models import UserProfile, User
from accounts.serializers.user_serializer import UserSerializer
from core.serializers.base_model_serializer import BaseModelSerializer


class UserProfileSerializer(BaseModelSerializer):
    """
    Serializer para el perfil del trader.
    """

    # --- FK WRITE ---
    user_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        write_only=True,
        source='user'
    )

    # --- FK READ ---
    user = UserSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
