from django.db import models

from core.models.base_model import BaseModel
from trades.choices import TradeStatusChoices


class Trade(BaseModel):
    """
    Representa un trade lógico completo dentro del sistema.

    Un Trade agrupa múltiples eventos de entrada (scaling in) y múltiples
    eventos de cierre (cierres parciales o totales), reflejando el
    comportamiento real de los mercados y plataformas como MT5 o Binance.

    Responsabilidades de negocio:
    - Agrupar aperturas y cierres bajo una misma operación lógica.
    - Mantener el estado general del trade.
    - Servir como punto central para análisis y métricas.

    Relaciones:
    - Pertenece a una TradeAccount.
    - Puede estar asociado a una TradingSignal.
    - Puede tener múltiples TradeEntry.
    - Puede tener múltiples TradeClose.
    """

    status = models.CharField(max_length=20, choices=TradeStatusChoices.choices, default=TradeStatusChoices.OPEN)
    opened_at = models.DateTimeField()
    closed_at = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)

    # FK
    trade_account = models.ForeignKey(
        'trades.TradeAccount',
        on_delete=models.CASCADE,
        related_name='trades'
    )
    trading_signal = models.ForeignKey(
        'signals.TradingSignal',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='trades'
    )
    asset = models.ForeignKey(
        'assets.Asset',
        on_delete=models.PROTECT,
        related_name='trades'
    )

    def __str__(self):
        return f"Trade {self.asset.symbol} ({self.status})"
