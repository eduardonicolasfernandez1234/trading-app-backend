from rest_framework import viewsets

from trades.models import TradeCost
from trades.serializers import TradeCostSerializer


class TradeCostViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar costos asociados a trades o cierres.
    """
    queryset = TradeCost.objects.all()
    serializer_class = TradeCostSerializer
