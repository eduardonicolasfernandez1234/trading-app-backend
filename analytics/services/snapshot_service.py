from decimal import Decimal

from django.db.models import QuerySet

from analytics.models import AnalyticsSnapshot
from analytics.services.drawdown_service import DrawdownService
from analytics.services.equity_curve_service import EquityCurveService
from analytics.services.trade_metrics_service import TradeMetricsService


class SnapshotService:
    """
    Servicio para generar snapshots consolidados de rendimiento.
    """

    @staticmethod
    def generate_snapshot(
            *,
            user,
            trades: QuerySet,
            snapshot_type: str,
            period_start,
            period_end,
            initial_balance: Decimal
    ) -> AnalyticsSnapshot:
        equity_curve = EquityCurveService.build_equity_curve(
            trades=list(trades),
            initial_balance=initial_balance
        )

        net_profit = equity_curve[-1]['equity'] - initial_balance if equity_curve else Decimal('0')
        max_drawdown = DrawdownService.calculate_max_drawdown(equity_curve)

        winning_trades = sum(
            1 for t in trades if TradeMetricsService.calculate_trade_pnl(t) > 0
        )

        snapshot = AnalyticsSnapshot.objects.create(
            user=user,
            period_start=period_start,
            period_end=period_end,
            snapshot_type=snapshot_type,
            total_trades=trades.count(),
            winning_trades=winning_trades,
            losing_trades=trades.count() - winning_trades,
            win_rate=(winning_trades / trades.count() * 100) if trades.exists() else 0,
            net_profit=net_profit,
            max_drawdown_percent=max_drawdown
        )

        return snapshot
