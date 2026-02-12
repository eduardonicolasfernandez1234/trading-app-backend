from rest_framework import viewsets

from accounts.models import UserNotificationSetting
from accounts.serializers import UserNotificationSettingSerializer


class UserNotificationSettingViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar configuraciones de notificaciones del usuario.
    """
    queryset = UserNotificationSetting.objects.all()
    serializer_class = UserNotificationSettingSerializer
