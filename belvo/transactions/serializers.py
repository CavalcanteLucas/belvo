from rest_framework import serializers

from django.db.utils import IntegrityError

from belvo.transactions.models import Transaction


class TransactionListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        transactions = [Transaction(**item) for item in validated_data]
        return Transaction.objects.bulk_create(transactions, ignore_conflicts=True)


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
        list_serializer_class = TransactionListSerializer
