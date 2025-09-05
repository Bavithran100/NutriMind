from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from logs.views import DailyLogViewSet
from users.views import register_user, login_user, user_profile
from food_suggestions.views import FoodSuggestionViewSet
from reports.views import ChatMessageViewSet

router = DefaultRouter()
router.register(r'logs', DailyLogViewSet, basename='logs')
router.register(r'food-suggestions', FoodSuggestionViewSet, basename='food-suggestions')
router.register(r'chat', ChatMessageViewSet, basename='chat')

def api_root(request):
    return JsonResponse({
        "message": "Mood & Food Wellness API",
        "version": "1.0.0",
        "endpoints": {
            "register": "/api/register/",
            "login": "/api/login/",
            "profile": "/api/profile/",
            "logs": "/api/logs/",
            "food_suggestions": "/api/food-suggestions/",
            "token_refresh": "/api/token/refresh/"
        }
    })

urlpatterns = [
    path('', api_root, name='api-root'),
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/register/', register_user, name='register'),
    path('api/login/', login_user, name='login'),
    path('api/profile/', user_profile, name='profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
