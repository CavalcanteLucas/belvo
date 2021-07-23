from rest_framework import serializers

from belvo.transactions.models import Transaction


class TransactionListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        unique_references = list(
            {transaction["reference"]: transaction for transaction in validated_data}
        )

        transactions = [
            next(
                transaction
                for transaction in validated_data
                if transaction["reference"] == reference
            )
            for reference in unique_references
        ]

        new_transactions = [
            Transaction(**transaction)
            for transaction in transactions
            if not Transaction.objects.filter(
                reference=transaction["reference"]
            ).exists()
        ]

        return Transaction.objects.bulk_create(new_transactions, ignore_conflicts=True)


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = "__all__"
        list_serializer_class = TransactionListSerializer
