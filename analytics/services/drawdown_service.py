from decimal import Decimal
from typing import List, Dict


class DrawdownService:
    """
    Servicio para calcular drawdown máximo basado en una curva de equity.
    """

    @staticmethod
    def calculate_max_drawdown(equity_curve: List[Dict]) -> Decimal:
        peak = None
        max_drawdown = Decimal('0')

        for point in equity_curve:
            equity = point['equity']

            if peak is None or equity > peak:
                peak = equity

            drawdown = (peak - equity) / peak * 100
            max_drawdown = max(max_drawdown, drawdown)

        return max_drawdown
