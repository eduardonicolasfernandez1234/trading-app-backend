from django.db import models

from core.models.base_model import BaseModel


class Asset(BaseModel):
    """
    Representa un activo financiero operable dentro del sistema.

    Un Asset define instrumentos como pares de divisas, commodities,
    criptomonedas o índices que pueden ser utilizados en señales y ejecuciones.

    Ejemplos:
    - XAUUSD
    - EURUSD
    - BTCUSD

    Responsabilidades de negocio:
    - Servir como referencia común para señales y ejecuciones.
    - Definir propiedades técnicas como valor del pip y decimales.
    - Permitir validaciones específicas por activo.

    Relaciones:
    - Pertenece a un AssetType.
    - Puede estar asociado a múltiples TradingSignals.
    - Puede tener múltiples configuraciones de horarios y swaps.
    """

    symbol = models.CharField(
        max_length=20,
        unique=True,
        help_text='Símbolo del activo (ej: XAUUSD, EURUSD)'
    )

    name = models.CharField(
        max_length=100,
        help_text='Nombre descriptivo del activo'
    )

    pip_value = models.DecimalField(
        max_digits=10,
        decimal_places=5,
        help_text='Valor monetario de un pip por lote estándar'
    )

    price_decimals = models.PositiveSmallIntegerField(
        default=2,
        help_text='Cantidad de decimales del precio'
    )

    is_tradable = models.BooleanField(
        default=True,
        help_text='Indica si el activo se puede operar actualmente'
    )

    # FK
    asset_type = models.ForeignKey(
        'assets.AssetType',
        on_delete=models.PROTECT,
        related_name='assets'
    )

    def __str__(self):
        return self.symbol
