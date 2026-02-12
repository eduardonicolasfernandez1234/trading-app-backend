from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

from accounts.viewsets import (
    UserViewSet,
    UserProfileViewSet,
    UserTradingPreferenceViewSet,
    UserRiskProfileViewSet,
    UserNotificationSettingViewSet,
)
from accounts.viewsets.jwt_view import EmailTokenObtainPairView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'user-profiles', UserProfileViewSet)
router.register(r'user-trading-preferences', UserTradingPreferenceViewSet)
router.register(r'user-risk-profiles', UserRiskProfileViewSet)
router.register(r'user-notification-settings', UserNotificationSettingViewSet)

urlpatterns = [
    path('token/', EmailTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns += router.urls
