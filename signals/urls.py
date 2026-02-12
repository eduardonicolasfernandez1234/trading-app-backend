from rest_framework.routers import DefaultRouter

from signals.viewsets import (
    SignalSourceViewSet,
    SignalProviderViewSet,
    TradingSignalViewSet,
    SignalTakeProfitViewSet,
    SignalContextViewSet,
)

router = DefaultRouter()
router.register(r'signal-sources', SignalSourceViewSet)
router.register(r'signal-providers', SignalProviderViewSet)
router.register(r'trading-signals', TradingSignalViewSet)
router.register(r'signal-take-profits', SignalTakeProfitViewSet)
router.register(r'signal-contexts', SignalContextViewSet)

urlpatterns = router.urls
