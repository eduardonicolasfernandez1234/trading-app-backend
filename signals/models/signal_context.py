from django.db import models

from core.models.base_model import BaseModel
from signals.choices import MarketConditionChoices, VolatilityLevelChoices
from .trading_signal import TradingSignal


class SignalContext(BaseModel):
    """
        Almacena información contextual adicional del mercado asociada a una señal
        de trading.

        SignalContext enriquece una TradingSignal con datos cualitativos que no
        siempre están presentes en la señal original, pero que son clave para
        análisis avanzados y automatización.

        Responsabilidades de negocio:
        - Registrar condiciones de mercado (tendencia o rango).
        - Identificar niveles de volatilidad y relación con noticias.
        - Proveer metadata útil para filtros, bots y reglas automáticas.

        Relaciones:
        - Mantiene una relación uno a uno con una TradingSignal.

        Valor estratégico:
        - Permite filtrar señales de baja calidad automáticamente.
        - Sirve como base para sistemas algorítmicos y de IA.
        - Ayuda a identificar bajo qué condiciones las señales funcionan mejor.
    """

    market_condition = models.CharField(
        max_length=20,
        choices=MarketConditionChoices.choices,
        null=True,
        blank=True
    )
    volatility_level = models.CharField(
        max_length=20,
        choices=VolatilityLevelChoices.choices,
        null=True,
        blank=True
    )
    news_related = models.BooleanField(default=False)
    commentary = models.TextField(blank=True)

    #FK
    trading_signal = models.OneToOneField(TradingSignal, on_delete=models.CASCADE, related_name='context')

    class Meta:
        verbose_name = 'Signal Context'
        verbose_name_plural = 'Signal Contexts'

    def __str__(self):
        return f"Context for {self.trading_signal_id}"
