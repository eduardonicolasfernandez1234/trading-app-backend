from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Autenticación usando email y contraseña.
    Devuelve access, refresh, id, email y role del usuario.
    """

    username_field = 'email'

    def validate(self, attrs):
        # super() handles authentication and raises AuthenticationFailed on invalid credentials
        data = super().validate(attrs)
        data['id'] = self.user.id
        data['email'] = self.user.email
        data['role'] = self.user.role
        return data
