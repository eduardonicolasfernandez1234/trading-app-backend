from django.db import models

from core.models.base_model import BaseModel


class AssetTradingSchedule(BaseModel):
    """
    Define los días y horarios en los que un activo puede ser operado.

    Este modelo es clave para validar señales, ejecuciones y automatizaciones,
    ya que no todos los activos operan los mismos días ni en los mismos horarios.

    Ejemplo:
    - XAUUSD: Lunes a Viernes
    - Crypto: Lunes a Domingo

    Responsabilidades de negocio:
    - Validar si una señal fue emitida en horario válido.
    - Evitar ejecuciones fuera de mercado.
    - Soportar análisis por sesiones y días.

    Relaciones:
    - Pertenece a un Asset.
    """

    day_of_week = models.PositiveSmallIntegerField(
        help_text='0=Lunes, 6=Domingo'
    )

    start_time = models.TimeField(
        help_text='Hora de inicio del trading'
    )

    end_time = models.TimeField(
        help_text='Hora de fin del trading'
    )

    # FK
    asset = models.ForeignKey(
        'assets.Asset',
        on_delete=models.CASCADE,
        related_name='trading_schedules'
    )

    class Meta:
        unique_together = ('asset', 'day_of_week', 'start_time')

    def __str__(self):
        return f"{self.asset.symbol} - Day {self.day_of_week}"
