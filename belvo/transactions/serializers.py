from rest_framework import serializers

from belvo.transactions.models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [
            "reference",
            "account",
            "date",
            "amount",
            "type",
            "category",
            "user_id",
        ]
