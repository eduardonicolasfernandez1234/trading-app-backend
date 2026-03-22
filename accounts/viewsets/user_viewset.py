from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from accounts.models import User
from accounts.serializers import UserSerializer, RegisterSerializer, ChangePasswordSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar usuarios del sistema.

    Endpoints estándar (CRUD):
        GET    /users/           -> listar usuarios
        POST   /users/           -> crear usuario (sin validación de contraseña, usar /register/)
        GET    /users/{id}/      -> detalle de un usuario
        PUT    /users/{id}/      -> actualizar usuario
        PATCH  /users/{id}/      -> actualizar parcialmente
        DELETE /users/{id}/      -> eliminar usuario (soft delete)

    Endpoints de autenticación / perfil:
        POST   /users/register/          -> registrar nuevo usuario (público)
        GET    /users/me/                -> obtener usuario autenticado
        PATCH  /users/me/                -> actualizar datos del usuario autenticado
        POST   /users/me/change-password/ -> cambiar contraseña
        POST   /users/logout/            -> invalidar refresh token (cerrar sesión)
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer

    # ── Registro ───────────────────────────────────────────────────────────────

    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        POST /api/accounts/users/register/

        Crea una cuenta nueva. No requiere autenticación.

        Body:
            email       (string, requerido)
            password    (string, requerido, mínimo 8 caracteres)
            password2   (string, requerido, debe coincidir con password)
            role        (string, opcional: admin|analyst|trader — default: trader)

        Respuesta 201: objeto User creado.
        Respuesta 400: errores de validación.
        """
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    # ── Usuario actual ─────────────────────────────────────────────────────────

    @action(detail=False, methods=['get', 'patch'], permission_classes=[IsAuthenticated])
    def me(self, request):
        """
        GET  /api/accounts/users/me/   -> datos del usuario autenticado
        PATCH /api/accounts/users/me/  -> actualizar email o role

        Requiere: Authorization: Bearer <access_token>

        Body (solo para PATCH, campos opcionales):
            email  (string)
            role   (string: admin|analyst|trader)
        """
        if request.method == 'GET':
            return Response(UserSerializer(request.user).data)

        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    # ── Cambio de contraseña ───────────────────────────────────────────────────

    @action(
        detail=False,
        methods=['post'],
        url_path='me/change-password',
        permission_classes=[IsAuthenticated],
    )
    def change_password(self, request):
        """
        POST /api/accounts/users/me/change-password/

        Cambia la contraseña del usuario autenticado.
        Requiere: Authorization: Bearer <access_token>

        Body:
            current_password  (string, requerido)
            new_password      (string, requerido, mínimo 8 caracteres)
            new_password2     (string, requerido, debe coincidir)

        Respuesta 200: { "detail": "Contraseña actualizada correctamente." }
        Respuesta 400: errores de validación o contraseña actual incorrecta.
        """
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        if not user.check_password(serializer.validated_data['current_password']):
            return Response(
                {'current_password': 'La contraseña actual es incorrecta.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'detail': 'Contraseña actualizada correctamente.'})

    # ── Logout ─────────────────────────────────────────────────────────────────

    @action(detail=False, methods=['post'], permission_classes=[IsAuthenticated])
    def logout(self, request):
        """
        POST /api/accounts/users/logout/

        Invalida el refresh token (blacklist). El access token sigue válido
        hasta su expiración, pero no se podrá renovar.
        Requiere: Authorization: Bearer <access_token>

        Body:
            refresh  (string, requerido — el refresh token a invalidar)

        Respuesta 200: { "detail": "Sesión cerrada correctamente." }
        Respuesta 400: token inválido o ya expirado.
        """
        refresh_token = request.data.get('refresh')
        if not refresh_token:
            return Response(
                {'detail': 'El campo refresh es requerido.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            return Response(
                {'detail': 'Token inválido o ya expirado.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({'detail': 'Sesión cerrada correctamente.'})
