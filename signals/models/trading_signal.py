from django.db import models

from assets.models import Asset
from core.models.base_model import BaseModel
from signals.choices import (
    DirectionChoices,
    SignalStatusChoices,
    ExecutionTypeChoices,
    MarketSessionChoices,
    ConfidenceLevelChoices,
)
from .signal_provider import SignalProvider
from .signal_source import SignalSource


class TradingSignal(BaseModel):
    """
        Representa una señal de trading tal como fue emitida originalmente por una
        fuente o proveedor de señales.

        TradingSignal es la entidad central del módulo de señales y funciona como
        referencia para ejecución, análisis, métricas y automatización futura.

        Responsabilidades de negocio:
        - Almacenar la intención original de la operación (BUY/SELL, entrada, SL).
        - Conservar el momento real en que la señal fue enviada, independiente de
          cuándo se registró en el sistema.
        - Actuar como entidad padre para niveles de take profit y contexto de mercado.
        - Permitir la comparación entre la calidad de la señal y la ejecución real.

        Relaciones:
        - Pertenece a una SignalSource.
        - Opcionalmente pertenece a un SignalProvider.
        - Está asociada a un Asset.
        - Puede tener múltiples SignalTakeProfit.
        - Puede tener un único SignalContext asociado.

        Notas importantes:
        - El campo `signal_time` representa cuándo se emitió la señal.
        - Este modelo no representa una operación ejecutada.
          La ejecución pertenece al dominio de trades.
    """

    direction = models.CharField(
        max_length=10,
        choices=DirectionChoices.choices
    )
    entry_price = models.DecimalField(max_digits=12, decimal_places=5)
    stop_loss = models.DecimalField(max_digits=12, decimal_places=5)
    execution_type = models.CharField(
        max_length=10,
        choices=ExecutionTypeChoices.choices,
        default=ExecutionTypeChoices.MARKET
    )
    confidence_level = models.CharField(
        max_length=10,
        choices=ConfidenceLevelChoices.choices,
        null=True,
        blank=True
    )
    session = models.CharField(
        max_length=20,
        choices=MarketSessionChoices.choices,
        null=True,
        blank=True
    )
    timeframe = models.CharField(
        max_length=10,
        blank=True,
        help_text='M1, M5, M15, H1, etc.'
    )
    signal_time = models.DateTimeField(
        help_text='Original signal time (when it was sent)'
    )
    status = models.CharField(
        max_length=20,
        choices=SignalStatusChoices.choices,
        default=SignalStatusChoices.ACTIVE
    )
    raw_message = models.TextField(
        blank=True,
        help_text='Original signal message'
    )

    # FK
    signal_source = models.ForeignKey(SignalSource, on_delete=models.CASCADE, related_name='signals')
    signal_provider = models.ForeignKey(
        SignalProvider,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='signals'
    )
    asset = models.ForeignKey(Asset, on_delete=models.PROTECT, related_name='signals')

    class Meta:
        verbose_name = 'Trading Signal'
        verbose_name_plural = 'Trading Signals'

    def __str__(self):
        return f"{self.asset.symbol} {self.direction.upper()} @ {self.entry_price}"
