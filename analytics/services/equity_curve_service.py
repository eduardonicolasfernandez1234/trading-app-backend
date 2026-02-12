from decimal import Decimal
from typing import List, Dict
from trades.models import Trade
from analytics.services.trade_metrics_service import TradeMetricsService


class EquityCurveService:
    """
    Servicio para construir la curva de equity basada en
    resultados reales o simulados trade por trade.
    """

    @staticmethod
    def build_equity_curve(
        trades: List[Trade],
        initial_balance: Decimal
    ) -> List[Dict]:
        """
        Devuelve una lista de puntos de equity en el tiempo.
        """
        equity = initial_balance
        curve = []

        for trade in trades:
            pnl = TradeMetricsService.calculate_trade_pnl(trade)
            equity += pnl

            curve.append({
                'trade_id': trade.id,
                'closed_at': trade.closed_at,
                'pnl': pnl,
                'equity': equity
            })

        return curve
