from rest_framework.routers import DefaultRouter

from assets.viewsets import (
    AssetTypeViewSet,
    AssetViewSet,
    AssetTradingScheduleViewSet,
    AssetSwapViewSet,
)

router = DefaultRouter()
router.register(r'asset-types', AssetTypeViewSet)
router.register(r'assets', AssetViewSet)
router.register(r'asset-trading-schedules', AssetTradingScheduleViewSet)
router.register(r'asset-swaps', AssetSwapViewSet)

urlpatterns = router.urls
