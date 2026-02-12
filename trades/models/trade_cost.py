from django.db import models

from core.models.base_model import BaseModel
from trades.choices import TradeCostTypeChoices


class TradeCost(BaseModel):
    """
    Representa un costo asociado a un trade o a un evento específico.

    Permite registrar swap, comisiones u otros fees aplicados durante
    la vida del trade o en cierres individuales.

    Responsabilidades de negocio:
    - Registrar costos reales de operación.
    - Permitir análisis del impacto de costos.
    - Soportar cálculo real de PnL.

    Relaciones:
    - Puede pertenecer a un Trade o a un TradeClose.
    """
    cost_type = models.CharField(
        max_length=50,
        choices=TradeCostTypeChoices.choices,
        help_text='swap, commission, fee, etc.'
    )
    amount = models.DecimalField(max_digits=12, decimal_places=5)

    # FK
    trade = models.ForeignKey(
        'trades.Trade',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='costs'
    )
    trade_close = models.ForeignKey(
        'trades.TradeClose',
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='costs'
    )

    def __str__(self):
        return f"{self.cost_type}: {self.amount}"
