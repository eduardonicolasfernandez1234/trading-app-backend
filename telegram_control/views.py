import asyncio
import os
import sys

import psutil
from django.conf import settings
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from telethon import TelegramClient
from telethon.errors import (
    FloodWaitError,
    PhoneCodeExpiredError,
    PhoneCodeInvalidError,
    SessionPasswordNeededError,
)

from .models import TelegramAccount
from .serializers import TelegramAccountSerializer


def _make_client(account: TelegramAccount) -> TelegramClient:
    return TelegramClient(
        account.session_name,
        account.api_id,
        account.api_hash,
    )


class TelegramAccountViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar cuentas de Telegram.

    Cada cuenta tiene su propio ciclo de autenticacion y su propio
    proceso listener independiente.

    Flujo de uso:
        1. POST /api/telegram/accounts/                    -> crear cuenta
        2. POST /api/telegram/accounts/{id}/request-code/ -> pedir codigo
        3. POST /api/telegram/accounts/{id}/verify-code/  -> verificar codigo
        4. POST /api/telegram/accounts/{id}/connect/      -> iniciar listener
        5. POST /api/telegram/accounts/{id}/disconnect/   -> detener listener
    """

    queryset = TelegramAccount.objects.all()
    serializer_class = TelegramAccountSerializer

    # ── Autenticacion ──────────────────────────────────────────────────────────

    @action(detail=True, methods=['post'], url_path='request-code')
    def request_code(self, request, pk=None):
        """
        POST /api/telegram/accounts/{id}/request-code/

        Solicita a Telegram que envie el codigo de verificacion al numero
        configurado en la cuenta. El codigo llega como mensaje dentro
        de la app de Telegram.

        Usar cuando la sesion no existe o expiro.
        Si el listener esta corriendo, detenerlo primero con /disconnect/.
        """
        account = self.get_object()

        async def _request():
            client = _make_client(account)
            await client.connect()
            try:
                result = await client.send_code_request(account.phone_number)
                return result.phone_code_hash
            finally:
                await client.disconnect()

        try:
            phone_code_hash = asyncio.run(_request())
        except FloodWaitError as e:
            minutes, seconds = divmod(e.seconds, 60)
            return Response(
                {
                    "status": "error",
                    "code": "flood_wait",
                    "detail": f"Demasiados intentos. Espera {minutes}m {seconds}s.",
                    "wait_seconds": e.seconds,
                },
                status=status.HTTP_429_TOO_MANY_REQUESTS,
            )
        except Exception as e:
            return Response(
                {"status": "error", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        account.phone_code_hash = phone_code_hash
        account.awaiting_2fa = False
        account.save()

        return Response(
            {
                "status": "code_sent",
                "detail": "Codigo enviado. Buscalo como mensaje del contacto 'Telegram' en tu app.",
                "next_step": f"POST /api/telegram/accounts/{account.id}/verify-code/",
            }
        )

    @action(detail=True, methods=['post'], url_path='verify-code')
    def verify_code(self, request, pk=None):
        """
        POST /api/telegram/accounts/{id}/verify-code/
        Body: { "code": "12345" }

        Verifica el codigo recibido y crea la sesion autenticada.
        Si la cuenta tiene 2FA, devuelve status "2fa_required".
        """
        account = self.get_object()

        code = request.data.get("code", "").strip()
        if not code:
            return Response(
                {"status": "error", "detail": "El campo 'code' es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not account.phone_code_hash:
            return Response(
                {
                    "status": "error",
                    "detail": "No hay un codigo pendiente. Llama primero a /request-code/.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        async def _verify():
            client = _make_client(account)
            await client.connect()
            try:
                await client.sign_in(
                    account.phone_number,
                    code,
                    phone_code_hash=account.phone_code_hash,
                )
            finally:
                await client.disconnect()

        try:
            asyncio.run(_verify())

        except PhoneCodeInvalidError:
            return Response(
                {"status": "error", "code": "code_invalid", "detail": "El codigo es incorrecto."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        except PhoneCodeExpiredError:
            account.phone_code_hash = ""
            account.save()
            return Response(
                {
                    "status": "error",
                    "code": "code_expired",
                    "detail": "El codigo vencio. Llama a /request-code/ para solicitar uno nuevo.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        except SessionPasswordNeededError:
            account.awaiting_2fa = True
            account.save()
            return Response(
                {
                    "status": "2fa_required",
                    "detail": "La cuenta tiene verificacion en dos pasos. Envia la contrasena a /verify-2fa/.",
                    "next_step": f"POST /api/telegram/accounts/{account.id}/verify-2fa/",
                }
            )

        except Exception as e:
            return Response(
                {"status": "error", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        account.phone_code_hash = ""
        account.awaiting_2fa = False
        account.save()

        return Response(
            {
                "status": "authenticated",
                "detail": "Sesion creada correctamente.",
                "next_step": f"POST /api/telegram/accounts/{account.id}/connect/",
            }
        )

    @action(detail=True, methods=['post'], url_path='verify-2fa')
    def verify_2fa(self, request, pk=None):
        """
        POST /api/telegram/accounts/{id}/verify-2fa/
        Body: { "password": "tu_contrasena" }

        Completa la autenticacion para cuentas con verificacion en dos pasos.
        Solo necesario si /verify-code/ devolvio {"status": "2fa_required"}.
        """
        account = self.get_object()

        if not account.awaiting_2fa:
            return Response(
                {
                    "status": "error",
                    "detail": "No hay autenticacion 2FA pendiente para esta cuenta.",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        password = request.data.get("password", "").strip()
        if not password:
            return Response(
                {"status": "error", "detail": "El campo 'password' es requerido."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        async def _verify_2fa():
            client = _make_client(account)
            await client.connect()
            try:
                await client.sign_in(password=password)
            finally:
                await client.disconnect()

        try:
            asyncio.run(_verify_2fa())
        except Exception as e:
            return Response(
                {"status": "error", "detail": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        account.phone_code_hash = ""
        account.awaiting_2fa = False
        account.save()

        return Response(
            {
                "status": "authenticated",
                "detail": "Autenticacion 2FA completada.",
                "next_step": f"POST /api/telegram/accounts/{account.id}/connect/",
            }
        )

    # ── Control del listener ───────────────────────────────────────────────────

    @action(detail=True, methods=['post'])
    def connect(self, request, pk=None):
        """
        POST /api/telegram/accounts/{id}/connect/

        Inicia el proceso listener para esta cuenta como subproceso independiente.
        Cada cuenta corre su propio proceso.
        """
        account = self.get_object()

        if account.is_running:
            return Response(
                {"status": "already_running", "pid": account.pid},
                status=status.HTTP_200_OK,
            )

        if not account.is_authenticated:
            return Response(
                {
                    "status": "error",
                    "code": "no_session",
                    "detail": "La cuenta no esta autenticada.",
                    "next_step": f"POST /api/telegram/accounts/{account.id}/request-code/",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        process = psutil.Popen(
            [
                sys.executable, "-m", "telegram_listener.main",
                "--api-id", str(account.api_id),
                "--api-hash", account.api_hash,
                "--phone", account.phone_number,
                "--session", account.session_name,
                "--account-id", str(account.id),
            ],
            cwd=str(settings.BASE_DIR),
        )

        account.pid = process.pid
        account.save()

        return Response(
            {"status": "started", "pid": process.pid},
            status=status.HTTP_201_CREATED,
        )

    @action(detail=True, methods=['post'])
    def disconnect(self, request, pk=None):
        """
        POST /api/telegram/accounts/{id}/disconnect/

        Detiene el proceso listener de esta cuenta de forma ordenada.
        """
        account = self.get_object()

        if not account.is_running:
            account.pid = None
            account.save()
            return Response({"status": "not_running"}, status=status.HTTP_200_OK)

        try:
            proc = psutil.Process(account.pid)
            proc.terminate()
            proc.wait(timeout=10)
        except psutil.NoSuchProcess:
            pass
        except psutil.TimeoutExpired:
            proc.kill()

        account.pid = None
        account.save()

        return Response({"status": "stopped"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        """
        GET /api/telegram/accounts/{id}/status/

        Devuelve el estado completo de la cuenta:
        - is_authenticated: existe el archivo de sesion
        - is_running: el proceso listener esta activo
        - pending_auth: en que paso del auth esta (null / "code" / "2fa")
        """
        account = self.get_object()

        # Limpiar PID si el proceso ya no existe
        if account.pid is not None and not account.is_running:
            account.pid = None
            account.save()

        pending_auth = None
        if account.awaiting_2fa:
            pending_auth = "2fa"
        elif account.phone_code_hash:
            pending_auth = "code"

        return Response({
            "id": account.id,
            "name": account.name,
            "phone_number": account.phone_number,
            "is_authenticated": account.is_authenticated,
            "is_running": account.is_running,
            "pid": account.pid,
            "pending_auth": pending_auth,
        })
