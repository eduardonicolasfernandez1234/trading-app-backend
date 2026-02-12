from rest_framework import serializers

from accounts.models import UserNotificationSetting, User
from accounts.serializers.user_serializer import UserSerializer
from core.serializers.base_model_serializer import BaseModelSerializer


class UserNotificationSettingSerializer(BaseModelSerializer):
    """
    Serializer para configuración de notificaciones del usuario.
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
        model = UserNotificationSetting
        fields = '__all__'
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
