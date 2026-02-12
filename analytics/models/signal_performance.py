from django.db import models

from core.models.base_model import BaseModel


class SignalPerformance(BaseModel):
    """
    Representa el desempeño teórico de una señal de trading,
    independiente de la ejecución real de los usuarios.

    Este modelo permite evaluar la calidad objetiva de las
    señales emitidas por una fuente o proveedor.

    Responsabilidades de negocio:
    - Medir efectividad de señales.
    - Alimentar rankings de grupos y proveedores.
    - Servir como base para copy trading inteligente.

    Relaciones:
    - Mantiene relación uno a uno con una TradingSignal.
    """

    theoretical_pips = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    hit_take_profit = models.BooleanField(default=False)
    hit_stop_loss = models.BooleanField(default=False)

    max_favorable_excursion = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    max_adverse_excursion = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    # FK
    trading_signal = models.OneToOneField(
        'signals.TradingSignal',
        on_delete=models.CASCADE,
        related_name='signal_performance'
    )

    def __str__(self):
        return f"Signal Performance {self.trading_signal_id}"
