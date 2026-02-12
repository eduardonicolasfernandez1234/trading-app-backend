from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate


class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Autenticación usando email y contraseña.
    """

    username_field = 'email'

    def validate(self, attrs):
        credentials = {
            'email': attrs.get('email'),
            'password': attrs.get('password'),
        }

        user = authenticate(**credentials)

        if user is None:
            raise Exception('Credenciales inválidas')

        data = super().validate(attrs)
        data['email'] = user.email

        return data
