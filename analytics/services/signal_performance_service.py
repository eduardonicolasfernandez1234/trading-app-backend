from analytics.models import SignalPerformance
from signals.models import TradingSignal


class SignalPerformanceService:
    """
    Servicio para calcular el desempeño teórico de una señal.
    """

    @staticmethod
    def calculate_signal_performance(signal: TradingSignal) -> SignalPerformance:
        """
        Calcula el resultado teórico de una señal
        independiente de la ejecución del usuario.
        """
        # Placeholder: lógica real vendrá luego (TP/SL)
        performance, _ = SignalPerformance.objects.get_or_create(
            trading_signal=signal
        )
        return performance
