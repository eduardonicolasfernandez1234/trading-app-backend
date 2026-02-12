from django.db import models

from core.models.base_model import BaseModel


class UserProfile(BaseModel):
    """
    Representa el perfil personal y profesional del trader.

    Este modelo almacena información descriptiva que no forma
    parte del proceso de autenticación, pero es clave para
    contextualizar al usuario dentro del sistema.

    Responsabilidades de negocio:
    - Almacenar información personal del trader.
    - Servir como base para análisis de comportamiento.
    - Facilitar personalización del sistema.

    Relaciones:
    - Mantiene una relación uno a uno con User.
    """

    display_name = models.CharField(
        max_length=150,
        blank=True
    )

    country = models.CharField(
        max_length=100,
        blank=True
    )

    timezone = models.CharField(
        max_length=50,
        default='UTC'
    )

    experience_years = models.PositiveSmallIntegerField(
        default=0
    )

    notes = models.TextField(blank=True)

    # FK
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='profile'
    )

    def __str__(self):
        return self.display_name or self.user.username
