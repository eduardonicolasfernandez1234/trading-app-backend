from django.db import models

from core.models.base_model import BaseModel


class AssetType(BaseModel):
    """
    Representa el tipo o categoría de un activo financiero.

    Este modelo permite clasificar los activos según su mercado, lo que
    facilita validaciones, análisis y reglas específicas por tipo.

    Ejemplos:
    - Forex
    - Crypto
    - Commodities
    - Índices
    - Stocks

    Responsabilidades de negocio:
    - Clasificar activos por mercado.
    - Permitir análisis y reglas diferenciadas por tipo de activo.
    - Facilitar la expansión a nuevos mercados.

    Relaciones:
    - Un AssetType puede tener múltiples Assets asociados.
    """

    name = models.CharField(max_length=50, unique=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
