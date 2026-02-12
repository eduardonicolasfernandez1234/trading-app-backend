from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from signals.filters import SignalSourceFilter
from signals.models import SignalSource
from signals.serializers import SignalSourceSerializer


class SignalSourceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar fuentes de señales (grupos, canales, comunidades).
    """
    queryset = SignalSource.objects.all()
    serializer_class = SignalSourceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = SignalSourceFilter

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
