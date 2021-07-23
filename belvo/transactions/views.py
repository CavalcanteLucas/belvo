from rest_framework import generics

from belvo.transactions.models import Transaction
from belvo.transactions.serializers import TransactionSerializer


class TransactionCreateAPIView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def perform_create(self, serializer):
        serializer.save()
