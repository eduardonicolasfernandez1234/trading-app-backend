from decimal import Decimal

from django.utils.dateparse import parse_date
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from analytics.models import AnalyticsSnapshot
from analytics.serializers import AnalyticsSnapshotSerializer
from analytics.services.snapshot_service import SnapshotService
from trades.models import Trade


class AnalyticsSnapshotViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar snapshots históricos de métricas.

    Normalmente estos registros se crean por procesos automáticos,
    pero se exponen vía API para consulta y administración.
    """
    queryset = AnalyticsSnapshot.objects.all()
    serializer_class = AnalyticsSnapshotSerializer

    @action(detail=False, methods=['post'], url_path='generate-snapshot')
    def generate_snapshot(self, request):
        """
        Genera un snapshot de rendimiento basado en trades reales.
        """
        user = request.user

        snapshot_type = request.data.get('snapshot_type')
        initial_balance = Decimal(request.data.get('initial_balance'))
        period_start = parse_date(request.data.get('period_start'))
        period_end = parse_date(request.data.get('period_end'))

        trades = Trade.objects.filter(
            trade_account__user=user,
            closed_at__date__gte=period_start,
            closed_at__date__lte=period_end,
            status='closed'
        ).order_by('closed_at')

        snapshot = SnapshotService.generate_snapshot(
            user=user,
            trades=trades,
            snapshot_type=snapshot_type,
            period_start=period_start,
            period_end=period_end,
            initial_balance=initial_balance
        )

        serializer = self.get_serializer(snapshot)
        return Response(serializer.data)
