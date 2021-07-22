from django.urls import path

from .views import UserListAPIView, UserDetailAPIView

app_name = "users"
urlpatterns = [
    path("", UserListAPIView.as_view(), name="user"),
    path("<int:pk>/", UserDetailAPIView.as_view(), name="user_detail"),
]
