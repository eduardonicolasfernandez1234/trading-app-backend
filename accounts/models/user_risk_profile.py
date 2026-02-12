from django.db import models

from core.models.base_model import BaseModel


class UserRiskProfile(BaseModel):
    """
    Define el perfil de riesgo del usuario.

    Este modelo permite almacenar configuraciones de riesgo
    que pueden ser usadas como sugerencias o validaciones
    durante la ejecución de trades.

    Responsabilidades de negocio:
    - Definir límites de riesgo por trade.
    - Permitir cálculos sugeridos de lotaje.
    - Servir como base para alertas de riesgo.

    Relaciones:
    - Mantiene una relación uno a uno con User.
    """

    risk_per_trade_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Porcentaje del balance a arriesgar por trade'
    )

    max_daily_drawdown_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    max_open_trades = models.PositiveSmallIntegerField(
        default=5
    )

    use_risk_suggestions = models.BooleanField(
        default=True,
        help_text='Permite al sistema sugerir tamaño de lote'
    )

    # FK
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='risk_profile'
    )

    def __str__(self):
        return f"Risk Profile - {self.user.username}"
