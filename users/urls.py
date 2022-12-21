from rest_framework import routers
from django.urls import path, re_path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views
from versiones.v1.router import api_urlpatterns as api_v1
from versiones.v2.router import api_urlpatterns as api_v2

router = routers.DefaultRouter()
router.register('', views.GetUsers)

urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path("jwt/create/", TokenObtainPairView.as_view(), name="jwt_create"),
    path("jwt/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("jwt/verify/", TokenVerifyView.as_view(), name="token_verify"),
    re_path(r'^api/v1/', include(api_v1)),
    re_path(r'^api/v2/', include(api_v2)),
]

urlpatterns += router.urls