from rest_framework import generics
from rest_framework.response import Response

from belvo.users.models import User
from belvo.users.serializers import UserSerializer, BalanceSerializer, SummarySerializer
from belvo.transactions.models import Transaction, TransactionTypes
from belvo.transactions.serializers import TransactionSerializer


class UserListAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserBalanceAPIView(generics.ListAPIView):
    serializer_class = BalanceSerializer

    def get_result(self, data):
        result = list(
            {transaction["account"]: transaction for transaction in data}.values()
        )
        return result

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return Response(self.get_result(serializer.data))

    def get_queryset(self):
        user_id = self.kwargs["pk"]
        return Transaction.objects.filter(user_id=user_id)


class UserSummaryAPIView(generics.ListAPIView):
    serializer_class = SummarySerializer

    def get_result(self, data):
        return {
            TransactionTypes.INFLOW: {
                transaction["category"]: transaction["amount"]
                for transaction in data
                if transaction["type"] == TransactionTypes.INFLOW
                and float(transaction["amount"]) > 0
            },
            TransactionTypes.OUTFLOW: {
                transaction["category"]: transaction["amount"]
                for transaction in data
                if transaction["type"] == TransactionTypes.OUTFLOW
                and float(transaction["amount"]) < 0
            },
        }

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return Response(self.get_result(serializer.data))

    def get_queryset(self):
        user_id = self.kwargs["pk"]
        return Transaction.objects.filter(user_id=user_id).order_by('category')
