from rest_framework.routers import DefaultRouter

from .views import TelegramAccountViewSet

router = DefaultRouter()
router.register(r'accounts', TelegramAccountViewSet)

urlpatterns = router.urls
