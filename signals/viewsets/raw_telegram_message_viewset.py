from rest_framework import viewsets

from signals.models import RawTelegramMessage
from signals.serializers import RawTelegramMessageSerializer


class RawTelegramMessageViewSet(viewsets.ModelViewSet):
    queryset = RawTelegramMessage.objects.all()
    serializer_class = RawTelegramMessageSerializer
