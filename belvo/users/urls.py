from django.urls import path

from belvo.users.views import (
    UserListAPIView,
    UserDetailAPIView,
    UserBalanceAPIView,
    UserSummaryAPIView,
)

app_name = "users"
urlpatterns = [
    path("", UserListAPIView.as_view(), name="user"),
    path("<int:pk>/", UserDetailAPIView.as_view(), name="user_detail"),
    path("<int:pk>/balance/", UserBalanceAPIView.as_view(), name="user_balance"),
    path("<int:pk>/summary/", UserSummaryAPIView.as_view(), name="user_summary"),
]
