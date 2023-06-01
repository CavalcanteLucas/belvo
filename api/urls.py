from django.urls import path

from .views import (
    TransactionCreateAPIView,
    TransactionSummaryByTypePerUserAPIView,
    TransactionSummaryByCategoryForUserAPIView,
)

urlpatterns = [
    path(
        'transactions/',
        TransactionCreateAPIView.as_view(),
        name='transaction-create',
    ),
    path(
        'transactions/summary/type/',
        TransactionSummaryByTypePerUserAPIView.as_view(),
        name='transaction-summary-by-type-per-user',
    ),
    path(
        'transactions/summary/',
        TransactionSummaryByCategoryForUserAPIView.as_view(),
        name='transaction-category-summary',
    ),
]
