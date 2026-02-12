from decimal import Decimal
from typing import List, Dict

from analytics.services.drawdown_service import DrawdownService
from analytics.services.equity_curve_service import EquityCurveService
from trades.models import Trade


class ProjectionSimulationService:
    """
    Servicio para simular escenarios futuros de trading
    de forma realista, trade por trade.
    """

    @staticmethod
    def simulate(
            *,
            historical_trades: List[Trade],
            initial_balance: Decimal
    ) -> Dict:
        """
        Simula un escenario futuro replicando el comportamiento
        histórico trade por trade.
        """

        equity_curve = EquityCurveService.build_equity_curve(
            trades=historical_trades,
            initial_balance=initial_balance
        )

        max_drawdown = DrawdownService.calculate_max_drawdown(equity_curve)

        return {
            'final_balance': equity_curve[-1]['equity'] if equity_curve else initial_balance,
            'max_drawdown_percent': max_drawdown,
            'equity_curve': equity_curve,
        }
