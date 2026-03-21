from django.db import models

from core.models.base_model import BaseModel


class UserSignalStats(BaseModel):
    """
    Representa estadísticas agregadas de señales para un usuario
    en un periodo de tiempo específico.

    Este modelo permite analizar cómo le va a un usuario siguiendo
    señales de determinados grupos, proveedores o activos.

    Responsabilidades de negocio:
    - Medir efectividad del copy trading por usuario.
    - Comparar resultados entre fuentes y proveedores.
    - Alimentar dashboards personalizados.

    Relaciones:
    - Pertenece a un usuario.
    - Puede asociarse a una fuente, proveedor y cuenta de trading.
    """

    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    calculated_at = models.DateTimeField(auto_now=True)

    total_signals = models.PositiveIntegerField()
    followed_signals = models.PositiveIntegerField()
    profitable_signals = models.PositiveIntegerField()
    losing_signals = models.PositiveIntegerField(default=0)

    total_profit_loss = models.DecimalField(
        max_digits=15,
        decimal_places=2,
        default=0
    )

    average_profit = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    average_loss = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    total_pips = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )

    average_rr = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    # FK
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='signal_stats'
    )

    trade_account = models.ForeignKey(
        'trades.TradeAccount',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='signal_stats'
    )

    signal_source = models.ForeignKey(
        'signals.SignalSource',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='user_signal_stats'
    )

    signal_provider = models.ForeignKey(
        'signals.SignalProvider',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='user_signal_stats'
    )

    def __str__(self):
        return f"Stats {self.user.email} ({self.period_start} - {self.period_end})"
