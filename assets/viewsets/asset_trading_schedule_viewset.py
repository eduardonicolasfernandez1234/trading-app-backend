from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from assets.filters.asset_trading_schedule_filter import AssetTradingScheduleFilter
from assets.models import AssetTradingSchedule
from assets.serializers import AssetTradingScheduleSerializer


class AssetTradingScheduleViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar horarios de trading de los activos.
    """
    queryset = AssetTradingSchedule.objects.select_related('asset')
    serializer_class = AssetTradingScheduleSerializer

    filter_backends = [DjangoFilterBackend]
    filterset_class = AssetTradingScheduleFilter

    ordering_fields = [
        'day_of_week',
        'start_time',
        'end_time',
        'asset__symbol',
        'created_at',
    ]
    ordering = ['asset__symbol', 'day_of_week']

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
