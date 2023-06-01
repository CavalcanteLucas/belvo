from rest_framework import serializers

from .models import Transaction


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'

    def validate_reference(self, value):
        if len(value) != 6:
            raise serializers.ValidationError(
                {'reference': 'Reference must have exactly 6 characters'}
            )
        if Transaction.objects.filter(reference=value).exists():
            raise serializers.ValidationError(
                {'reference': 'Reference already exists'}
            )
        return value

    def validate(self, data):
        if data['type'] == 'outflow' and data['amount'] >= 0:
            raise serializers.ValidationError(
                {'amount': 'Outflow amount must be negative'}
            )
        elif data['type'] == 'inflow' and data['amount'] <= 0:
            raise serializers.ValidationError(
                {'amount': 'Inflow amount must be positive'}
            )
        return data


class TransactionSummaryByTypePerUserSerializer(serializers.Serializer):
    user_email = serializers.EmailField()
    total_inflow = serializers.DecimalField(max_digits=10, decimal_places=2)
    total_outflow = serializers.DecimalField(max_digits=10, decimal_places=2)


class TransactionSummaryByCategoryForUserSerializer(serializers.Serializer):
    inflow = serializers.DictField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2)
    )
    outflow = serializers.DictField(
        child=serializers.DecimalField(max_digits=10, decimal_places=2)
    )
