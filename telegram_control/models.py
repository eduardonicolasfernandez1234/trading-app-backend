import os
import re

import psutil
from django.conf import settings
from django.db import models

from core.models.base_model import BaseModel


class TelegramAccount(BaseModel):
    """
    Representa una cuenta de Telegram configurada para escuchar mensajes.

    Cada cuenta tiene sus propias credenciales (api_id, api_hash, phone_number)
    obtenidas desde my.telegram.org. Una cuenta puede estar autenticada (sesion
    existente), corriendo (proceso activo escuchando mensajes), o ambas.

    Responsabilidades:
    - Almacenar las credenciales de cada cuenta de Telegram.
    - Mantener el estado del proceso listener (PID).
    - Mantener el estado transitorio de autenticacion (phone_code_hash, 2FA).

    Notas de seguridad:
    - api_hash se almacena en texto plano (MVP). Agregar encriptacion en produccion.
    - phone_code_hash es temporal y se borra una vez completada la autenticacion.
    """

    name = models.CharField(
        max_length=150,
        help_text='Nombre descriptivo de la cuenta (ej: "Cuenta Principal")'
    )
    api_id = models.IntegerField(
        help_text='API ID obtenido desde my.telegram.org'
    )
    api_hash = models.CharField(
        max_length=64,
        help_text='API Hash obtenido desde my.telegram.org'
    )
    phone_number = models.CharField(
        max_length=20,
        unique=True,
        help_text='Numero de telefono con codigo de pais (ej: +59178535699)'
    )
    session_name = models.CharField(
        max_length=100,
        unique=True,
        editable=False,
        help_text='Nombre del archivo de sesion (auto-generado)'
    )

    # Estado del proceso listener (manejado por el sistema)
    pid = models.IntegerField(
        null=True,
        blank=True,
        editable=False,
        help_text='PID del proceso listener activo'
    )

    # Estado transitorio de autenticacion (se limpia al completar auth)
    phone_code_hash = models.CharField(
        max_length=128,
        blank=True,
        editable=False,
        help_text='Hash temporal del codigo enviado por Telegram'
    )
    awaiting_2fa = models.BooleanField(
        default=False,
        editable=False,
        help_text='Indica si la autenticacion esta esperando la contrasena 2FA'
    )

    class Meta:
        verbose_name = 'Telegram Account'
        verbose_name_plural = 'Telegram Accounts'

    def __str__(self):
        return f"{self.name} ({self.phone_number})"

    def save(self, *args, **kwargs):
        if not self.session_name:
            digits = re.sub(r'\D', '', self.phone_number)
            self.session_name = f"telegram_session_{digits}"
        super().save(*args, **kwargs)

    @property
    def session_file_path(self) -> str:
        return str(os.path.join(settings.BASE_DIR, f"{self.session_name}.session"))

    @property
    def is_authenticated(self) -> bool:
        return os.path.exists(self.session_file_path)

    @property
    def is_running(self) -> bool:
        return self.pid is not None and psutil.pid_exists(self.pid)
