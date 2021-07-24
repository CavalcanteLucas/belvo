from django.db import models

from belvo.users.models import User


class TransactionTypes(models.TextChoices):
    INFLOW = "inflow", "inflow"
    OUTFLOW = "outflow", "outflow"


class Transaction(models.Model):
    reference = models.CharField(max_length=6)
    account = models.CharField(max_length=6)
    date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    type = models.CharField(max_length=7, choices=TransactionTypes.choices)
    category = models.CharField(max_length=20)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                name="only_one_reference",
                fields=["reference"],
            ),
            models.CheckConstraint(
                name="only_two_types_of_transaction",
                check=models.Q(type__in=TransactionTypes.values),
            ),
            models.CheckConstraint(
                name="inflow_positive_or_outflow_negative",
                check=(
                    models.Q(type=TransactionTypes.INFLOW, amount__gte=0)
                    | models.Q(type=TransactionTypes.OUTFLOW, amount__lt=0)
                ),
            ),
        ]

    def __str__(self):
        return str(self.id)
