from django.db import models
from django.db.models.expressions import CombinedExpression, F

from belvo.users.models import User


class TransactionTypes(models.TextChoices):
    INFLOW = "IN", "inflow"
    OUTFLOW = "OU", "outflow"


class Transaction(models.Model):
    reference = models.CharField(max_length=6, unique=True)
    account = models.CharField(max_length=6)
    date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    type = models.CharField(max_length=7, choices=TransactionTypes.choices)
    category = models.CharField(max_length=20)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="only_two_types_of_transaction",
                check=models.Q(type__in=TransactionTypes.values),
            ),
            models.CheckConstraint(
                name="inflow_positive_or_outflow_negative",
                check=(
                    models.Q(type="IN", amount__gte=0)
                    | models.Q(type="OU", amount__lt=0)
                ),
            ),
        ]
