from rest_framework import serializers

from belvo.transactions.models import Transaction


class TransactionListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        unique_reference_transactions = list(
            {
                transaction["reference"]: transaction for transaction in validated_data
            }.values()
        )

        new_transactions = [
            Transaction(**transaction)
            for transaction in unique_reference_transactions
            if not Transaction.objects.filter(
                reference=transaction["reference"]
            ).exists()
        ]

        return Transaction.objects.bulk_create(new_transactions, ignore_conflicts=True)


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
