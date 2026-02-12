from rest_framework.routers import DefaultRouter

from analytics.viewsets import (
    AnalyticsSnapshotViewSet,
    SignalPerformanceViewSet,
    UserSignalStatsViewSet,
    ProjectionScenarioViewSet,
    AnalyticsRunViewSet,
)

router = DefaultRouter()
router.register(r'analytics-snapshots', AnalyticsSnapshotViewSet)
router.register(r'signal-performances', SignalPerformanceViewSet)
router.register(r'user-signal-stats', UserSignalStatsViewSet)
router.register(r'projection-scenarios', ProjectionScenarioViewSet)
router.register(r'analytics-runs', AnalyticsRunViewSet)

urlpatterns = router.urls
