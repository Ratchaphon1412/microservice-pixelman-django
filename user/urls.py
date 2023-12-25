
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView
)
from .views import *
urlpatterns = [
    path('token/', LoginAPIView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('profile/', UserProfilesAPIView.as_view(), name='profile'),
    path('address/', AddressAPIView.as_view(), name='address'),
]
