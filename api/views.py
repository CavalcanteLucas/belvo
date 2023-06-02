from django.db.models import Sum, When, Case, DecimalField
from rest_framework import generics, status
from rest_framework.response import Response
from decimal import Decimal, ROUND_DOWN

from .models import Transaction
from .serializers import (
    TransactionSerializer,
    TransactionSummaryByTypePerUserSerializer,
    TransactionSummaryByCategoryForUserSerializer,
)


class TransactionCreateAPIView(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    queryset = Transaction.objects.all()

    def create(self, request, *args, **kwargs):
        transactions_data = request.data
        if not isinstance(transactions_data, list):
            transactions_data = [transactions_data]

        transactions_to_create = []
        transactions_duplicated = []

        for transaction_data in transactions_data:
            reference = transaction_data['reference']
            user_email = transaction_data['user_email']
            transaction_instance = Transaction.objects.filter(
                reference=reference,
                user_email=user_email,
            ).first()

            if transaction_instance:
                transactions_duplicated.append(transaction_data)
            else:
                serializer = self.get_serializer(data=transaction_data)
                serializer.is_valid(raise_exception=True)
                transactions_to_create.append(serializer.validated_data)

        response_status = status.HTTP_200_OK
        if transactions_to_create:
            Transaction.objects.bulk_create(
                [Transaction(**data) for data in transactions_to_create]
            )
            response_status = status.HTTP_201_CREATED

        response_data = {
            'message': f'{len(transactions_to_create)} transaction(s) created',
            'created': [
                f'{transaction["reference"]} - {transaction["user_email"]}'
                for transaction in transactions_to_create
            ],
            'duplicates': [
                f'{transaction["reference"]} - {transaction["user_email"]}'
                for transaction in transactions_duplicated
            ],
        }

        return Response(response_data, status=response_status)


class TransactionSummaryByTypePerUserAPIView(generics.ListAPIView):
    serializer_class = TransactionSummaryByTypePerUserSerializer

    def get_queryset(self):
        queryset = Transaction.objects.values('user_email').annotate(
            total_inflow=Sum(
                Case(
                    When(type='inflow', then='amount'),
                    default=0,
                    output_field=DecimalField(),
                )
            ),
            total_outflow=Sum(
                Case(
                    When(type='outflow', then='amount'),
                    default=0,
                    output_field=DecimalField(),
                )
            ),
        )
        return queryset


class TransactionSummaryByCategoryForUserAPIView(generics.views.APIView):
    serializer_class = TransactionSummaryByCategoryForUserSerializer

    def get(self, request):
        user_email = request.query_params.get('user_email')
        inflow_summary = (
            Transaction.objects.filter(user_email=user_email, type='inflow')
            .values('category')
            .annotate(amount=Sum('amount'))
        )
        outflow_summary = (
            Transaction.objects.filter(user_email=user_email, type='outflow')
            .values('category')
            .annotate(amount=Sum('amount'))
        )

        inflow_dict = {}
        for item in inflow_summary:
            category = item['category']
            amount = Decimal(str(item['amount']))
            amount = amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
            inflow_dict[category] = amount

        outflow_dict = {}
        for item in outflow_summary:
            category = item['category']
            amount = Decimal(str(item['amount']))
            amount = amount.quantize(Decimal('0.00'), rounding=ROUND_DOWN)
            outflow_dict[category] = amount

        response_data = {
            'inflow': inflow_dict,
            'outflow': outflow_dict,
        }

        serializer = self.serializer_class(data=response_data)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
