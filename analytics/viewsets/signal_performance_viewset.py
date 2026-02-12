from rest_framework import viewsets

from analytics.models import SignalPerformance
from analytics.serializers import SignalPerformanceSerializer


class SignalPerformanceViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar el desempeño teórico de señales.

    Estos datos pueden ser calculados automáticamente o ajustados
    manualmente para análisis avanzados.
    """
    queryset = SignalPerformance.objects.all()
    serializer_class = SignalPerformanceSerializer
