from rest_framework import serializers

from django.db.models import Sum

from belvo.users.models import User
from belvo.transactions.models import Transaction, TransactionTypes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class BalanceSerializer(serializers.Serializer):
    account = serializers.CharField(max_length=6)
    balance = serializers.SerializerMethodField()
    total_inflow = serializers.SerializerMethodField()
    total_outflow = serializers.SerializerMethodField()

    def get_balance(self, obj):
        return (
            Transaction.objects.filter(account=obj.account).aggregate(Sum("amount"))[
                "amount__sum"
            ]
            or 0
        )

    def get_total_inflow(self, obj):
        return (
            Transaction.objects.filter(account=obj.account)
            .filter(type=TransactionTypes.INFLOW)
            .aggregate(Sum("amount"))["amount__sum"]
            or 0
        )

    def get_total_outflow(self, obj):
        return (
            Transaction.objects.filter(account=obj.account)
            .filter(type=TransactionTypes.OUTFLOW)
            .aggregate(Sum("amount"))["amount__sum"]
            or 0
        )


class SummarySerializer(serializers.Serializer):
    type = serializers.CharField(max_length=6)
    category = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=8, decimal_places=2)
