from rest_framework import viewsets

from trades.models import TradeClose
from trades.serializers import TradeCloseSerializer


class TradeCloseViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar cierres parciales o totales de trades.
    """
    queryset = TradeClose.objects.all()
    serializer_class = TradeCloseSerializer
