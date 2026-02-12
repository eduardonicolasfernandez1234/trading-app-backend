from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from signals.models import SignalContext
from signals.serializers import SignalContextSerializer


class SignalContextViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar el contexto de mercado de una señal.
    """
    queryset = SignalContext.objects.all()
    serializer_class = SignalContextSerializer

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
