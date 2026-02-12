from django.db import models

from core.models.base_model import BaseModel


class UserNotificationSetting(BaseModel):
    """
    Configura las preferencias de notificación del usuario.

    Este modelo prepara el sistema para alertas, bots y
    automatizaciones futuras.

    Responsabilidades de negocio:
    - Controlar qué eventos generan notificaciones.
    - Definir canales de notificación.
    - Evitar sobre-notificación.

    Relaciones:
    - Mantiene una relación uno a uno con User.
    """

    notify_trade_open = models.BooleanField(default=True)
    notify_trade_close = models.BooleanField(default=True)
    notify_drawdown_alert = models.BooleanField(default=True)

    email_notifications = models.BooleanField(default=True)
    push_notifications = models.BooleanField(default=False)

    # FK
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='notification_settings'
    )

    def __str__(self):
        return f"Notifications - {self.user.username}"
