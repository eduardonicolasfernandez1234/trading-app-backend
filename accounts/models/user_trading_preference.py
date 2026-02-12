from django.db import models

from core.models.base_model import BaseModel


class UserTradingPreference(BaseModel):
    """
    Almacena las preferencias operativas del usuario como trader.

    Este modelo define cómo el usuario prefiere operar, sin imponer
    reglas estrictas, permitiendo sugerencias y automatizaciones.

    Responsabilidades de negocio:
    - Definir horarios y estilos preferidos.
    - Configurar comportamiento por defecto del sistema.
    - Servir como base para filtros y recomendaciones.

    Relaciones:
    - Mantiene una relación uno a uno con User.
    """

    preferred_assets = models.JSONField(
        blank=True,
        default=list,
        help_text='Lista de símbolos preferidos (XAUUSD, BTCUSDT, etc.)'
    )

    preferred_sessions = models.JSONField(
        blank=True,
        default=list,
        help_text='Asia, London, New York'
    )

    allow_crypto = models.BooleanField(default=True)
    allow_forex = models.BooleanField(default=True)

    auto_close_enabled = models.BooleanField(
        default=False,
        help_text='Permite cierres automáticos por reglas'
    )

    # FK
    user = models.OneToOneField(
        'accounts.User',
        on_delete=models.CASCADE,
        related_name='trading_preferences'
    )

    def __str__(self):
        return f"Trading Preferences - {self.user.username}"
