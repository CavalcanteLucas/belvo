from django.db import models
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
            transaction_instance = Transaction.objects.filter(
                reference=transaction_data['reference'],
                user_email=transaction_data['user_email'],
            ).first()

            if transaction_instance:
                transactions_duplicated.append(transaction_data)
            else:
                serializer = self.get_serializer(data=transaction_data)
                serializer.is_valid(raise_exception=True)
                transactions_to_create.append(serializer.validated_data)

        if transactions_to_create:
            Transaction.objects.bulk_create(
                [Transaction(**data) for data in transactions_to_create]
            )

        response_data = {
            'message': f'{len(transactions_to_create)} transaction(s) created',
            'created': transactions_to_create,
            'duplicates': transactions_duplicated,
        }

        return Response(response_data, status=status.HTTP_201_CREATED)


class TransactionSummaryByTypePerUserAPIView(generics.ListAPIView):
    serializer_class = TransactionSummaryByTypePerUserSerializer

    def get_queryset(self):
        queryset = Transaction.objects.values('user_email').annotate(
            total_inflow=models.Sum(
                models.Case(
                    models.When(type='inflow', then='amount'),
                    default=0,
                    output_field=models.DecimalField(),
                )
            ),
            total_outflow=models.Sum(
                models.Case(
                    models.When(type='outflow', then='amount'),
                    default=0,
                    output_field=models.DecimalField(),
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
            .annotate(amount=models.Sum('amount'))
        )
        outflow_summary = (
            Transaction.objects.filter(user_email=user_email, type='outflow')
            .values('category')
            .annotate(amount=models.Sum('amount'))
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
