from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from assets.filters.asset_type_filter import AssetTypeFilter
from assets.models import AssetType
from assets.serializers import AssetTypeSerializer


class AssetTypeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar tipos de activos (Forex, Crypto, etc.).
    """
    queryset = AssetType.objects.all()
    serializer_class = AssetTypeSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = AssetTypeFilter

    ordering_fields = [
        'name',
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
