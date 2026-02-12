from accounts.models import User
from core.serializers.base_model_serializer import BaseModelSerializer


class UserSerializer(BaseModelSerializer):
    """
    Serializer para el usuario del sistema.

    Maneja información básica del usuario autenticado.
    La gestión de contraseña se realiza por mecanismos
    de autenticación (JWT / reset password).
    """

    class Meta:
        model = User
        fields = (
            'id',
            'email',
            'is_active',
            'is_staff',
            'is_superuser',
            'created_at',
            'updated_at',
        )
        read_only_fields = BaseModelSerializer.Meta.read_only_fields
