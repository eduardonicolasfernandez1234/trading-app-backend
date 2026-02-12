from decimal import Decimal

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from analytics.services.equity_curve_service import EquityCurveService
from analytics.services.trade_metrics_service import TradeMetricsService
from trades.models import Trade
from trades.models import TradeAccount
from trades.serializers import TradeAccountSerializer


class TradeAccountViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar cuentas de trading.
    """
    queryset = TradeAccount.objects.all()
    serializer_class = TradeAccountSerializer

    @action(detail=True, methods=['get'], url_path='equity')
    def equity(self, request, pk=None):
        """
        Devuelve la curva de equity actual de la cuenta.
        """
        account = self.get_object()

        trades = Trade.objects.filter(
            trade_account=account,
            status='closed'
        ).order_by('closed_at')

        curve = EquityCurveService.build_equity_curve(
            trades=list(trades),
            initial_balance=account.initial_balance
        )

        return Response({
            'account_id': account.id,
            'current_equity': curve[-1]['equity'] if curve else account.initial_balance,
            'equity_curve': curve
        })

    @action(detail=True, methods=['get'], url_path='summary')
    def summary(self, request, pk=None):
        """
        Devuelve un resumen general de la cuenta de trading.
        """
        account = self.get_object()

        trades = Trade.objects.filter(
            trade_account=account,
            status='closed'
        )

        pnl_list = [TradeMetricsService.calculate_trade_pnl(t) for t in trades]
        net_pnl = sum(pnl_list, Decimal('0'))

        equity_curve = EquityCurveService.build_equity_curve(
            trades=list(trades.order_by('closed_at')),
            initial_balance=account.initial_balance
        )

        wins = sum(1 for pnl in pnl_list if pnl > 0)

        return Response({
            'account_id': account.id,
            'initial_balance': account.initial_balance,
            'current_equity': equity_curve[-1]['equity'] if equity_curve else account.initial_balance,
            'total_trades': trades.count(),
            'winrate': (wins / trades.count() * 100) if trades.exists() else 0,
            'net_pnl': net_pnl
        })
