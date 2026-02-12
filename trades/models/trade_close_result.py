from django.db import models

from core.models.base_model import BaseModel


class TradeCloseResult(BaseModel):
    """
    Representa el resultado financiero de un evento de cierre específico.

    Permite calcular resultados de forma granular cuando existen cierres
    parciales, facilitando métricas precisas y recomputables.

    Responsabilidades de negocio:
    - Almacenar pips ganados o perdidos por cierre.
    - Registrar ganancia o pérdida monetaria.
    - Servir como base para métricas agregadas.

    Relaciones:
    - Mantiene relación uno a uno con un TradeClose.
    """
    pips_result = models.DecimalField(max_digits=10, decimal_places=2)
    profit_loss = models.DecimalField(max_digits=15, decimal_places=2)

    # FK
    trade_close = models.OneToOneField(
        'trades.TradeClose',
        on_delete=models.CASCADE,
        related_name='result'
    )

    def __str__(self):
        return f"Result {self.profit_loss}"
