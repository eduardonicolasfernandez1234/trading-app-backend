from django.db import models

from core.models.base_model import BaseModel
from trades.choices import TradeCloseReasonChoices


class TradeClose(BaseModel):
    """
    Representa un evento de cierre de posición, parcial o total.

    Un Trade puede tener múltiples TradeClose, permitiendo cierres parciales
    basados en lotaje, take profit, stop loss o cierre manual.

    Responsabilidades de negocio:
    - Registrar cada evento de cierre.
    - Almacenar precio, lote cerrado y motivo del cierre.
    - Diferenciar cierres manuales y automáticos.

    Relaciones:
    - Pertenece a un Trade.
    """

    CLOSE_REASON_CHOICES = (
        ('tp', 'Take Profit'),
        ('sl', 'Stop Loss'),
        ('manual', 'Manual'),
        ('bot', 'Bot'),
    )

    close_price = models.DecimalField(max_digits=12, decimal_places=5)
    lot_size = models.DecimalField(max_digits=10, decimal_places=2, help_text='Cantidad de lote cerrada en este evento')
    closed_at = models.DateTimeField()
    close_reason = models.CharField(max_length=10, choices=TradeCloseReasonChoices.choices)
    external_close_id = models.CharField(max_length=100, blank=True)

    # FK
    trade = models.ForeignKey(
        'trades.Trade',
        on_delete=models.CASCADE,
        related_name='closes'
    )

    def __str__(self):
        return f"Close @ {self.close_price} ({self.lot_size})"
