"""
Script de autenticacion con Telegram.

Ejecutar una sola vez para crear el archivo telegram_session.session:
    python -m telegram_listener.auth

Una vez autenticado, usar el listener normal:
    python -m telegram_listener.main
"""

import asyncio
import logging
import os

from telethon import TelegramClient
from telethon.errors import (
    FloodWaitError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
)

from telegram_listener.config.settings import get_settings

# Logging detallado para ver exactamente que esta pasando
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

settings = get_settings()

SESSION_FILE = "telegram_session"


async def authenticate():
    # Borrar sesion previa si existe y esta corrupta
    session_path = f"{SESSION_FILE}.session"
    if os.path.exists(session_path):
        logger.info(f"Sesion existente encontrada: {session_path}")
        answer = input("Existe una sesion previa. Borrarla y reautenticar? (s/n): ").strip().lower()
        if answer == "s":
            os.remove(session_path)
            logger.info("Sesion borrada. Iniciando nueva autenticacion.")
        else:
            logger.info("Usando sesion existente.")

    client = TelegramClient(SESSION_FILE, settings.API_ID, settings.API_HASH)

    await client.connect()
    logger.info("Conectado a los servidores de Telegram.")

    if await client.is_user_authorized():
        me = await client.get_me()
        logger.info(f"Ya autenticado como: {me.first_name} (@{me.username})")
        await client.disconnect()
        print("\nYa estas autenticado. Podes correr el listener con:")
        print("    python -m telegram_listener.main")
        return

    # Solicitar el codigo
    logger.info(f"Solicitando codigo para el numero: {settings.PHONE_NUMBER}")
    try:
        await client.send_code_request(settings.PHONE_NUMBER)
        logger.info("Solicitud de codigo enviada.")
        print("\nEl codigo fue enviado a tu aplicacion de Telegram.")
        print("Buscalo como un mensaje del contacto 'Telegram' dentro de la app.")
        print("(NO llega por SMS si ya tenes Telegram instalado en el celular)\n")
    except FloodWaitError as e:
        logger.error(f"FloodWaitError: Telegram te bloqueo por {e.seconds} segundos ({e.seconds // 60} minutos).")
        print(f"\nERROR: Hiciste demasiados intentos. Telegram te bloqueo por {e.seconds} segundos.")
        print(f"Espera {e.seconds // 60} minutos y {e.seconds % 60} segundos antes de volver a intentar.")
        await client.disconnect()
        return

    # Pedir el codigo al usuario
    code = input("Ingresa el codigo que recibiste en Telegram: ").strip()

    try:
        await client.sign_in(settings.PHONE_NUMBER, code)
        me = await client.get_me()
        logger.info(f"Autenticacion exitosa como: {me.first_name} (@{me.username})")
        print(f"\nAutenticado correctamente como {me.first_name}!")
        print("Ahora podes correr el listener con:")
        print("    python -m telegram_listener.main")

    except PhoneCodeInvalidError:
        logger.error("El codigo ingresado es incorrecto.")
        print("\nERROR: El codigo es incorrecto. Volvé a ejecutar este script.")

    except PhoneCodeExpiredError:
        logger.error("El codigo expiro.")
        print("\nERROR: El codigo expiro. Volvé a ejecutar este script para solicitar uno nuevo.")

    except SessionPasswordNeededError:
        # La cuenta tiene 2FA activado
        logger.info("La cuenta tiene 2FA activado. Solicitando contrasena.")
        print("\nTu cuenta tiene verificacion en dos pasos (2FA) activada.")
        password = input("Ingresa tu contrasena de Telegram: ").strip()
        try:
            await client.sign_in(password=password)
            me = await client.get_me()
            logger.info(f"Autenticacion con 2FA exitosa como: {me.first_name}")
            print(f"\nAutenticado correctamente como {me.first_name}!")
        except Exception as e:
            logger.error(f"Error en 2FA: {e}")
            print(f"\nERROR en 2FA: {e}")

    finally:
        await client.disconnect()


if __name__ == "__main__":
    asyncio.run(authenticate())
