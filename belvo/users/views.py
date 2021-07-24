from datetime import datetime

from rest_framework import generics
from rest_framework.response import Response

from belvo.users.models import User
from belvo.users.serializers import UserSerializer, SummarySerializer
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
    serializer_class = TransactionSerializer

    def get_result(self, data):
        unique_transactions = list(
            {transaction["reference"]: transaction for transaction in data}.values()
        )

        unique_accounts = []
        [
            ""
            for transaction in data
            if not (
                transaction["account"] in unique_accounts
                or unique_accounts.append(transaction["account"])
            )
        ]

        amount_per_account = []
        for account in unique_accounts:
            amount = []
            for transaction in unique_transactions:
                if transaction["account"] == account:
                    amount.append(float(transaction["amount"]))
            amount_per_account.append({account: amount})

        result = []
        for item in amount_per_account:
            account = list(item.keys()).pop()
            amounts = list(item.values()).pop()
            balance = sum(amounts)
            total_inflow = sum(amount for amount in amounts if amount > 0)
            total_outflow = sum(amount for amount in amounts if amount < 0)
            result.append(
                {
                    "account": account,
                    "balance": "%.2f" % balance,
                    "total_inflow": "%.2f" % total_inflow,
                    "total_outflow": "%.2f" % total_outflow,
                }
            )

        return result

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()

        serializer = self.get_serializer(queryset, many=True)
        return Response(self.get_result(serializer.data))

    def get_queryset(self):
        user_id = self.kwargs["pk"]
        start = self.request.GET.get("start", "2020-01-01")
        end = self.request.GET.get("end", str(datetime.now().date()))
        return (
            Transaction.objects.filter(user_id=user_id)
            .filter(date__range=[start, end])
            .order_by("account")
        )


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
        return Transaction.objects.filter(user_id=user_id).order_by("category")
