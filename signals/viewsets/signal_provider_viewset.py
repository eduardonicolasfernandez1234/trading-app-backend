from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from signals.filters import SignalProviderFilter
from signals.models import SignalProvider
from signals.serializers import SignalProviderSerializer


class SignalProviderViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar proveedores/instructores de señales.
    """
    queryset = SignalProvider.objects.select_related('signal_source')
    serializer_class = SignalProviderSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = SignalProviderFilter

    ordering_fields = [
        'name',
        'alias',
        'is_anonymous',
        'experience_level',
        'signal_source__name',
        'created_at',
    ]
    ordering = ['name']

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
