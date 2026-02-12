from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from assets.filters.asset_swap_filter import AssetSwapFilter
from assets.models import AssetSwap
from assets.serializers import AssetSwapSerializer


class AssetSwapViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar configuración de swaps de los activos.
    """
    queryset = AssetSwap.objects.select_related('asset')
    serializer_class = AssetSwapSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = AssetSwapFilter

    ordering_fields = [
        'swap_long',
        'swap_short',
        'triple_swap_day',
        'asset__symbol',
        'created_at',
    ]
    ordering = ['asset__symbol']

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
