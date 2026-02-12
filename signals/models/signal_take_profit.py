from django.db import models

from core.models.base_model import BaseModel
from .trading_signal import TradingSignal


class SignalTakeProfit(BaseModel):
    """
       Representa un nivel de take profit (objetivo de ganancia) asociado a una
       señal de trading.

       Una TradingSignal puede definir múltiples niveles de take profit, lo que
       permite salidas parciales o escalonadas de una operación.

       Responsabilidades de negocio:
       - Almacenar niveles de take profit ordenados (TP1, TP2, TP3, etc.).
       - Permitir cierres parciales mediante porcentajes sugeridos.
       - Facilitar el análisis de qué niveles de TP se alcanzan con mayor frecuencia.

       Relaciones:
       - Pertenece a una única TradingSignal.

       Consideraciones de diseño:
       - El campo `level` define el orden del take profit.
       - Este modelo es independiente del resultado real de la operación.
   """

    price = models.DecimalField(max_digits=12, decimal_places=5)
    level = models.PositiveSmallIntegerField(
        help_text='TP level (1, 2, 3, etc.)'
    )
    percentage_close = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        help_text='Percentage of position to close'
    )

    # FK
    trading_signal = models.ForeignKey(TradingSignal, on_delete=models.CASCADE, related_name='take_profits')

    class Meta:
        verbose_name = 'Signal Take Profit'
        verbose_name_plural = 'Signal Take Profits'
        ordering = ['level']
        unique_together = ('trading_signal', 'level')

    def __str__(self):
        return f"TP{self.level} @ {self.price}"
