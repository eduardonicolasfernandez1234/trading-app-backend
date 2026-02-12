from decimal import Decimal

from django.utils.dateparse import parse_datetime
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from analytics.services.trade_metrics_service import TradeMetricsService
from trades.models import Trade
from trades.models import TradeClose, TradeCloseResult
from trades.serializers import TradeSerializer


class TradeViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar trades (contenedor lógico de entradas y cierres).
    """
    queryset = Trade.objects.all()
    serializer_class = TradeSerializer

    @action(detail=True, methods=['post'], url_path='recalculate')
    def recalculate(self, request, pk=None):
        """
        Recalcula métricas de un trade basado en cierres y costos.
        """
        trade = self.get_object()

        pnl = TradeMetricsService.calculate_trade_pnl(trade)
        duration = TradeMetricsService.calculate_trade_duration_minutes(trade)

        return Response({
            'trade_id': trade.id,
            'pnl': pnl,
            'duration_minutes': duration
        })

    @action(detail=True, methods=['post'], url_path='close')
    def close_trade(self, request, pk=None):
        """
        Cierra completamente un trade.
        Puede ser ejecutado por sistema o usuario.
        """
        trade = self.get_object()

        price = Decimal(request.data.get('price'))
        lot_closed = Decimal(request.data.get('lot_closed'))
        reason = request.data.get('reason', 'manual')
        closed_at = parse_datetime(request.data.get('closed_at'))

        close = TradeClose.objects.create(
            trade=trade,
            price=price,
            lot_closed=lot_closed,
            close_reason=reason,
            closed_at=closed_at,
            executed_by='system' if reason == 'system' else 'manual'
        )

        # Resultado financiero
        pnl = TradeMetricsService.calculate_trade_pnl(trade)

        TradeCloseResult.objects.create(
            trade_close=close,
            profit_loss=pnl
        )

        trade.status = 'closed'
        trade.closed_at = closed_at
        trade.save(update_fields=['status', 'closed_at'])

        return Response({
            'trade_id': trade.id,
            'status': 'closed',
            'pnl': pnl
        })

    @action(detail=True, methods=['post'], url_path='partial-close')
    def partial_close(self, request, pk=None):
        """
        Realiza un cierre parcial de un trade.
        """
        trade = self.get_object()

        price = Decimal(request.data.get('price'))
        lot_closed = Decimal(request.data.get('lot_closed'))
        reason = request.data.get('reason', 'manual')
        closed_at = parse_datetime(request.data.get('closed_at'))

        close = TradeClose.objects.create(
            trade=trade,
            price=price,
            lot_closed=lot_closed,
            close_reason=reason,
            closed_at=closed_at,
            executed_by='system' if reason == 'system' else 'manual'
        )

        pnl = TradeMetricsService.calculate_trade_pnl(trade)

        TradeCloseResult.objects.create(
            trade_close=close,
            profit_loss=pnl
        )

        return Response({
            'trade_id': trade.id,
            'closed_lot': lot_closed,
            'remaining_lot': trade.remaining_lot,
            'pnl_so_far': pnl
        })
