from decimal import Decimal
from trades.models import Trade, TradeClose, TradeCost


class TradeMetricsService:
    """
    Servicio encargado de calcular métricas reales por trade
    basadas en aperturas, cierres parciales y costos.
    """

    @staticmethod
    def calculate_trade_pnl(trade: Trade) -> Decimal:
        """
        Calcula el profit/loss total de un trade considerando:
        - cierres parciales
        - costos (swap, comisión, fees)
        """
        closes = TradeClose.objects.filter(trade=trade)
        total_pnl = Decimal('0')

        for close in closes:
            if hasattr(close, 'result'):
                total_pnl += close.result.profit_loss

        costs = TradeCost.objects.filter(trade=trade)
        for cost in costs:
            total_pnl -= cost.amount

        return total_pnl

    @staticmethod
    def calculate_trade_duration_minutes(trade: Trade) -> int:
        """
        Calcula la duración total del trade en minutos.
        """
        if not trade.closed_at:
            return 0

        delta = trade.closed_at - trade.opened_at
        return int(delta.total_seconds() / 60)
