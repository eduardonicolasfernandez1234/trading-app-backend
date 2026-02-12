from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from assets.filters.asset_filter import AssetFilter
from assets.models import Asset
from assets.serializers import AssetSerializer


class AssetViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar activos operables (XAUUSD, BTCUSDT, etc.).
    """
    queryset = Asset.objects.select_related('asset_type')
    serializer_class = AssetSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = AssetFilter

    ordering_fields = [
        'symbol',
        'name',
        'pip_value',
        'price_decimals',
        'is_tradable',
        'asset_type__name',
        'created_at',
    ]
    ordering = ['symbol']

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
