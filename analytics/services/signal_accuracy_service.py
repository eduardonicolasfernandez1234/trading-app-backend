from analytics.services.trade_metrics_service import TradeMetricsService
from signals.models import TradingSignal
from trades.models import Trade


class SignalAccuracyService:
    """
    Servicio para calcular métricas de precisión de señales.
    """

    @staticmethod
    def accuracy_by_signal_source(signal_source):
        signals = TradingSignal.objects.filter(
            signal_source=signal_source
        )

        total = signals.count()
        wins = 0

        for signal in signals:
            trades = Trade.objects.filter(
                trading_signal=signal,
                status='closed'
            )

            for trade in trades:
                pnl = TradeMetricsService.calculate_trade_pnl(trade)
                if pnl > 0:
                    wins += 1
                    break

        return {
            'signal_source': signal_source.name,
            'total_signals': total,
            'winning_signals': wins,
            'accuracy_percent': (wins / total * 100) if total else 0
        }

    @staticmethod
    def accuracy_by_provider(provider):
        signals = TradingSignal.objects.filter(
            signal_provider=provider
        )

        total = signals.count()
        wins = 0

        for signal in signals:
            trades = Trade.objects.filter(
                trading_signal=signal,
                status='closed'
            )

            for trade in trades:
                pnl = TradeMetricsService.calculate_trade_pnl(trade)
                if pnl > 0:
                    wins += 1
                    break

        return {
            'provider': provider.name,
            'total_signals': total,
            'winning_signals': wins,
            'accuracy_percent': (wins / total * 100) if total else 0
        }
