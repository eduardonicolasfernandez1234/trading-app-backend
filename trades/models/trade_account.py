from django.db import models

from core.models.base_model import BaseModel


class TradeAccount(BaseModel):
    """
    Representa una cuenta de trading utilizada para ejecutar operaciones.

    Permite separar resultados por broker, tipo de cuenta o capital inicial,
    siendo clave para análisis de rendimiento y gestión de riesgo.

    Responsabilidades de negocio:
    - Identificar la cuenta donde se ejecutan los trades.
    - Permitir métricas y análisis por cuenta.
    - Soportar múltiples cuentas simultáneamente (demo, real, copy).

    Relaciones:
    - Una TradeAccount puede tener múltiples Trades.
    """

    name = models.CharField(max_length=100)
    broker = models.CharField(max_length=100)
    initial_balance = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.CharField(max_length=10, default='USD')
    is_demo = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} ({self.broker})"
