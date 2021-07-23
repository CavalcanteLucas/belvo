from rest_framework import generics, status
from rest_framework.response import Response

from belvo.transactions.models import Transaction
from belvo.transactions.serializers import TransactionSerializer


class TransactionCreateAPIView(generics.CreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_serializer(self, *args, **kwargs):
        if "data" in kwargs:
            data = kwargs["data"]
            if isinstance(data, list):
                kwargs["many"] = True

        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save()
