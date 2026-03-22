from django.contrib.auth.models import AbstractUser
from django.db import models

from accounts.choices import UserRoleChoices
from core.managers.custom_user_manager import CustomUserManager
from core.models import BaseModel


class User(AbstractUser, BaseModel):
    """
    Representa al usuario autenticado del sistema.

    Este modelo extiende el usuario base de Django y sirve como
    entidad principal de autenticación y autorización.

    Responsabilidades de negocio:
    - Autenticación del usuario.
    - Asociación con perfiles, preferencias y cuentas de trading.
    - Control de acceso al sistema.

    Nota:
    - Este modelo no contiene lógica de trading.
    - La lógica operativa vive en modelos relacionados.
    """

    username = models.CharField(max_length=150, unique=False, blank=True, null=True)
    email = models.EmailField(unique=True)
    role = models.CharField(
        max_length=20,
        choices=UserRoleChoices.choices,
        default=UserRoleChoices.TRADER
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    # Override the SoftDeleteManager inherited from BaseModel so that
    # create_user() and create_superuser() remain available.
    objects = CustomUserManager()

    def __str__(self):
        return self.email
