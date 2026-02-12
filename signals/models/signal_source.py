from django.db import models

from core.models.base_model import BaseModel
from signals.choices import PlatformChoices, SignalStyleChoices, RiskProfileChoices


class SignalSource(BaseModel):
    """
        Representa una fuente de señales de trading, como un grupo, canal o comunidad
        externa (por ejemplo: Telegram, Discord, WhatsApp).

        Una SignalSource es el nivel más alto de origen de las señales y se utiliza
        como unidad principal para análisis globales de rendimiento y comparación.

        Responsabilidades de negocio:
        - Agrupar señales de trading bajo un mismo origen.
        - Permitir el análisis de rentabilidad, consistencia y drawdown por fuente.
        - Proveer contexto adicional como estilo de trading, perfil de riesgo,
          zona horaria e idioma.

        Relaciones:
        - Una SignalSource puede tener múltiples SignalProviders.
        - Una SignalSource puede emitir múltiples TradingSignals.

        Nota de diseño:
        - Este modelo no representa usuarios del sistema.
        - Modela entidades externas dentro del ecosistema de trading.
    """

    name = models.CharField(max_length=150)
    platform = models.CharField(
        max_length=20,
        choices=PlatformChoices.choices
    )
    description = models.TextField(blank=True)
    is_private = models.BooleanField(default=True)
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        help_text='Timezone of the signal source'
    )
    language = models.CharField(
        max_length=10,
        default='es'
    )
    signal_style = models.CharField(
        max_length=20,
        choices=SignalStyleChoices.choices,
        null=True,
        blank=True
    )
    risk_profile = models.CharField(
        max_length=20,
        choices=RiskProfileChoices.choices,
        null=True,
        blank=True
    )

    class Meta:
        verbose_name = 'Signal Source'
        verbose_name_plural = 'Signal Sources'

    def __str__(self):
        return self.name
