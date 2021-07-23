from rest_framework import generics

from django.db.utils import IntegrityError

from belvo.transactions.models import Transaction
from belvo.transactions.serializers import TransactionSerializer

from pprint import pprint


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
        if type(serializer.validated_data) == list:
            redundant_data = []
            for item in serializer.validated_data:
                if Transaction.objects.filter(reference=item["reference"]).exists():
                    redundant_data.append(item)
            for item in redundant_data:
                serializer.validated_data.remove(item)

        serializer.save()
