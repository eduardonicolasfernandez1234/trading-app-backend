from django.db import models

from core.models.base_model import BaseModel


class AssetSwap(BaseModel):
    """
    Define los valores de swap aplicables a un activo cuando una operación
    permanece abierta más de un día.

    Este modelo es especialmente importante para operaciones swing o de largo
    plazo, donde el swap puede afectar significativamente el resultado final.

    Responsabilidades de negocio:
    - Registrar swap long y short por activo.
    - Permitir el cálculo correcto de costos de operación.
    - Facilitar análisis de rentabilidad real en trades prolongados.

    Relaciones:
    - Pertenece a un Asset.
    """

    swap_long = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        help_text='Swap aplicado a posiciones BUY'
    )

    swap_short = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        help_text='Swap aplicado a posiciones SELL'
    )

    triple_swap_day = models.PositiveSmallIntegerField(
        default=2,
        help_text='Día de triple swap (por defecto miércoles = 2)'
    )

    # FK
    asset = models.ForeignKey(
        'assets.Asset',
        on_delete=models.CASCADE,
        related_name='swaps'
    )

    def __str__(self):
        return f"Swap {self.asset.symbol}"
