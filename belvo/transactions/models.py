from django.db import models

from belvo.users.models import User

TRANSACTION_TYPES = [
    ("INFLOW", "inflow"),
    ("OUTFLOW", "outflow"),
]


class Transaction(models.Model):
    reference = models.CharField(max_length=6, unique=True)
    account = models.CharField(max_length=6)
    date = models.DateField()
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    type = models.CharField(max_length=7, choices=TRANSACTION_TYPES)
    category = models.CharField(max_length=20)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
