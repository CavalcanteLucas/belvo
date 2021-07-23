from django.urls import path

from belvo.transactions.views import TransactionCreateAPIView

app_name = "transactions"
urlpatterns = [path("", TransactionCreateAPIView.as_view(), name="transaction")]
