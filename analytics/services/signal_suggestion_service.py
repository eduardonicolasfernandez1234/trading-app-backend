class SignalSuggestionService:
    """
    Servicio para generar sugerencias de decisión.
    """

    @staticmethod
    def should_ignore(signal_accuracy, threshold=40):
        """
        Sugiere ignorar una señal si la precisión histórica
        es menor al threshold.
        """
        return signal_accuracy < threshold
