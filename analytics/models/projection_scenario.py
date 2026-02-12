from django.db import models

from core.models.base_model import BaseModel


class ProjectionScenario(BaseModel):
    """
    Representa un escenario de simulación futura basado en
    datos históricos de trading.

    Este modelo permite a cada usuario evaluar posibles
    resultados antes de aplicar decisiones reales.

    Responsabilidades de negocio:
    - Simular crecimiento de capital.
    - Evaluar drawdown esperado.
    - Comparar estrategias de riesgo.

    Relaciones:
    - Pertenece a un usuario.
    - Puede basarse en una fuente de señales.
    """

    initial_balance = models.DecimalField(
        max_digits=15,
        decimal_places=2
    )

    risk_per_trade_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2
    )

    projection_days = models.PositiveIntegerField()

    expected_return = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True
    )

    expected_drawdown_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True
    )

    notes = models.TextField(blank=True)

    # FK
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='projection_scenarios'
    )

    signal_source = models.ForeignKey(
        'signals.SignalSource',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='projection_scenarios'
    )

    def __str__(self):
        return f"Projection {self.user.email}"
