from rest_framework import viewsets

from analytics.models import AnalyticsRun
from analytics.serializers import AnalyticsRunSerializer


class AnalyticsRunViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar ejecuciones de procesos analíticos.

    Útil para auditoría, debugging y monitoreo en entornos SaaS.
    """
    queryset = AnalyticsRun.objects.all()
    serializer_class = AnalyticsRunSerializer
