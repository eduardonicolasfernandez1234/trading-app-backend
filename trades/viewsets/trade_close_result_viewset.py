from rest_framework import viewsets

from trades.models import TradeCloseResult
from trades.serializers import TradeCloseResultSerializer


class TradeCloseResultViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar resultados financieros por cierre de trade.
    """
    queryset = TradeCloseResult.objects.all()
    serializer_class = TradeCloseResultSerializer
