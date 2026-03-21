from django.db import models


class UserRoleChoices(models.TextChoices):
    """
    Roles disponibles en la plataforma.

    ADMIN    — Administrador total. Puede gestionar usuarios, fuentes, señales,
               activos y toda la configuración de la plataforma.

    ANALYST  — Analista de señales. Puede registrar y gestionar SignalSources,
               SignalProviders y TradingSignals. No gestiona cuentas ni trades
               propios. Ideal para quien cuida la calidad de las señales.

    TRADER   — Trader estándar. Puede registrar sus propias cuentas de trading,
               sus trades y seguir señales. Es el perfil del usuario operativo.
    """
    ADMIN = 'admin', 'Administrador'
    ANALYST = 'analyst', 'Analista'
    TRADER = 'trader', 'Trader'
