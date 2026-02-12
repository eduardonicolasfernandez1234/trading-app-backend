from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from signals.models import SignalTakeProfit
from signals.serializers import SignalTakeProfitSerializer


class SignalTakeProfitViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar niveles de take profit de una señal.
    """
    queryset = SignalTakeProfit.objects.all()
    serializer_class = SignalTakeProfitSerializer

    @action(detail=False, methods=['get'], url_path='quick-search')
    def quick_search(self, request):
        """
        Endpoint optimizado para inputs de búsqueda rápida.
        - Sin paginación
        - Máx 30 registros
        - Con filtros + search
        """
        queryset = self.filter_queryset(self.get_queryset())[:30]
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
