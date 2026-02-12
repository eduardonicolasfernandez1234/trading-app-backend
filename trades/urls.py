from rest_framework.routers import DefaultRouter

from trades.viewsets import (
    TradeAccountViewSet,
    TradeViewSet,
    TradeEntryViewSet,
    TradeCloseViewSet,
    TradeCloseResultViewSet,
    TradeCostViewSet,
)

router = DefaultRouter()
router.register(r'trade-accounts', TradeAccountViewSet)
router.register(r'trades', TradeViewSet)
router.register(r'trade-entries', TradeEntryViewSet)
router.register(r'trade-closes', TradeCloseViewSet)
router.register(r'trade-close-results', TradeCloseResultViewSet)
router.register(r'trade-costs', TradeCostViewSet)

urlpatterns = router.urls
