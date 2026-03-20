from django.db import models

from core.models.base_model import BaseModel


class RawTelegramMessage(BaseModel):
    """
    Almacena mensajes de Telegram en bruto, sin procesar.

    Representa cada mensaje recibido desde cualquier canal o grupo
    al que el usuario esté suscrito. El texto crudo se conserva
    intacto para su posterior análisis (ej: parsing con IA).

    Responsabilidades:
    - Registrar todos los mensajes entrantes desde Telegram.
    - Servir como fuente para el proceso de parsing/clasificación futuro.
    - Evitar duplicados mediante la unicidad de (channel_id, telegram_message_id).
    """

    telegram_message_id = models.BigIntegerField(
        help_text='Telegram internal message ID'
    )
    channel_id = models.BigIntegerField(
        help_text='Telegram chat/channel ID'
    )
    channel_title = models.CharField(
        max_length=255,
        blank=True,
        help_text='Display name of the chat or channel'
    )
    channel_username = models.CharField(
        max_length=100,
        blank=True,
        help_text='@username of the channel (if public)'
    )
    sender_id = models.BigIntegerField(
        null=True,
        blank=True,
        help_text='Telegram ID of the sender (null for anonymous channels)'
    )
    sender_name = models.CharField(
        max_length=255,
        blank=True,
        help_text='Display name of the sender'
    )
    raw_text = models.TextField(
        help_text='Full original message text'
    )
    message_date = models.DateTimeField(
        help_text='Timestamp when Telegram sent the message'
    )
    chat_type = models.CharField(
        max_length=20,
        blank=True,
        help_text='channel / group / private'
    )
    telegram_account_id = models.IntegerField(
        null=True,
        blank=True,
        help_text='ID de la TelegramAccount que recibio este mensaje'
    )

    class Meta:
        verbose_name = 'Raw Telegram Message'
        verbose_name_plural = 'Raw Telegram Messages'
        unique_together = ('channel_id', 'telegram_message_id')
        ordering = ['-message_date']

    def __str__(self):
        prefix = self.channel_title or str(self.channel_id)
        return f"[{prefix}] {self.raw_text[:60]}"
