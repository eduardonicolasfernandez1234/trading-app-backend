from django.db import models

from core.models.base_model import BaseModel


class AnalyticsRun(BaseModel):
    """
    Representa una ejecución de análisis o cálculo de métricas.

    Este modelo permite auditar cuándo, cómo y para quién se
    ejecutaron procesos analíticos, especialmente útil en
    entornos SaaS y automatizados.

    Responsabilidades de negocio:
    - Registrar ejecuciones de analytics.
    - Auditar procesos automáticos o manuales.
    - Facilitar debugging y monitoreo.

    Relaciones:
    - Pertenece a un usuario.
    """

    ANALYSIS_TYPE_CHOICES = (
        ('snapshot', 'Snapshot'),
        ('ranking', 'Ranking'),
        ('projection', 'Projection'),
    )

    analysis_type = models.CharField(
        max_length=20,
        choices=ANALYSIS_TYPE_CHOICES
    )

    executed_at = models.DateTimeField()
    execution_time_ms = models.PositiveIntegerField()

    success = models.BooleanField(default=True)
    error_message = models.TextField(blank=True)

    # FK
    user = models.ForeignKey(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='analytics_runs'
    )

    def __str__(self):
        return f"{self.analysis_type} - {self.user.email}"
