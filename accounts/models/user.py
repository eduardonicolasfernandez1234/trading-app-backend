from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
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

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
