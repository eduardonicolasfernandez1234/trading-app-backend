from rest_framework import viewsets

from trades.models import TradeEntry
from trades.serializers import TradeEntrySerializer


class TradeEntryViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar aperturas de trades (scaling in).
    """
    queryset = TradeEntry.objects.all()
    serializer_class = TradeEntrySerializer
