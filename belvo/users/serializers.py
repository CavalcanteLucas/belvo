from rest_framework import serializers

from django.db.models import Sum

from belvo.users.models import User
from belvo.transactions.models import Transaction, TransactionTypes


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class SummarySerializer(serializers.Serializer):
    type = serializers.CharField(max_length=6)
    category = serializers.CharField(max_length=20)
    amount = serializers.DecimalField(max_digits=8, decimal_places=2)
