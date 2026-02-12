from django.db import models

from core.models.base_model import BaseModel
from trades.choices import TradeEntrySourceChoices


class TradeEntry(BaseModel):
    """
    Representa un evento de apertura de posición dentro de un trade.

    Un Trade puede tener múltiples TradeEntry, permitiendo estrategias de
    scaling in (entradas parciales o progresivas).

    Responsabilidades de negocio:
    - Registrar cada entrada al mercado.
    - Almacenar precio real, lote y origen de la apertura.
    - Preparar integración con brokers externos (MT5, Binance).

    Relaciones:
    - Pertenece a un Trade.
    """

    ENTRY_SOURCE_CHOICES = (
        ('manual', 'Manual'),
        ('bot', 'Bot'),
        ('api', 'API'),
    )

    entry_price = models.DecimalField(max_digits=12, decimal_places=5)
    lot_size = models.DecimalField(max_digits=10, decimal_places=2)
    opened_at = models.DateTimeField()
    entry_source = models.CharField(
        max_length=10,
        choices=TradeEntrySourceChoices.choices,
        default=TradeEntrySourceChoices.MANUAL
    )
    external_entry_id = models.CharField(max_length=100, blank=True, help_text='ID externo del broker (MT5, Binance)')

    # FK
    trade = models.ForeignKey(
        'trades.Trade',
        on_delete=models.CASCADE,
        related_name='entries'
    )

    def __str__(self):
        return f"Entry @ {self.entry_price} ({self.lot_size})"
