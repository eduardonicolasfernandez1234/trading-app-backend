from django.db import models

from core.models.base_model import BaseModel
from .signal_source import SignalSource


class SignalProvider(BaseModel):
    """
        Representa a una persona, instructor o identidad que emite señales de trading
        dentro de una fuente de señales específica.

        Un SignalProvider puede corresponder a una persona real, un alias o una
        identidad anónima. Este modelo permite un análisis más detallado de la
        calidad de las señales más allá del grupo o canal.

        Responsabilidades de negocio:
        - Asociar señales de trading a un proveedor específico cuando exista.
        - Comparar desempeño entre distintos proveedores dentro de una misma fuente.
        - Almacenar observaciones cualitativas o nivel de experiencia del proveedor.

        Relaciones:
        - Pertenece a una única SignalSource.
        - Puede estar asociado a múltiples TradingSignals.

        Nota de diseño:
        - No es un usuario autenticado del sistema.
        - Su propósito es únicamente analítico.
    """
    name = models.CharField(max_length=150)
    alias = models.CharField(
        max_length=150,
        blank=True,
        help_text='Nickname or username'
    )
    is_anonymous = models.BooleanField(default=False)
    experience_level = models.CharField(
        max_length=50,
        blank=True,
        help_text='Beginner / Pro / Unknown'
    )
    notes = models.TextField(blank=True)

    # FK
    signal_source = models.ForeignKey(SignalSource, on_delete=models.CASCADE, related_name='providers')

    class Meta:
        verbose_name = 'Signal Provider'
        verbose_name_plural = 'Signal Providers'
        unique_together = ('name', 'signal_source')

    def __str__(self):
        return self.name
