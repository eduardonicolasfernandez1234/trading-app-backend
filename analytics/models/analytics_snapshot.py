from django.db import models

from core.models.base_model import BaseModel


class AnalyticsSnapshot(BaseModel):
    """
    Representa una captura histórica de métricas de rendimiento
    de un usuario en un periodo de tiempo específico.

    Este modelo permite almacenar métricas consolidadas para
    evitar recalcular constantemente datos históricos y
    habilitar comparaciones temporales.

    Responsabilidades de negocio:
    - Guardar métricas agregadas por periodo.
    - Facilitar dashboards históricos.
    - Mejorar performance del sistema.

    Relaciones:
    - Pertenece a un usuario.
    """

    SNAPSHOT_TYPE_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
    )

    period_start = models.DateField()
    period_end = models.DateField()

    snapshot_type = models.CharField(
        max_length=20,
        choices=SNAPSHOT_TYPE_CHOICES
    )

    total_trades = models.PositiveIntegerField()
    winning_trades = models.PositiveIntegerField()
    losing_trades = models.PositiveIntegerField()

    win_rate = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    net_profit = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    max_drawdown_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    notes = models.TextField(blank=True)

    # FK
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='analytics_snapshots'
    )

    def __str__(self):
        return f"{self.user.email} - {self.snapshot_type} ({self.period_start})"
