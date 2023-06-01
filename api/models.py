from django.db import models


class Transaction(models.Model):
    reference = models.CharField(max_length=6)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(
        max_length=10,
        choices=[
            ('inflow', 'Inflow'),
            ('outflow', 'Outflow'),
        ],
    )
    category = models.CharField(max_length=20)
    user_email = models.EmailField()

    def __str__(self):
        return f'<Transaction reference={self.reference} user_email={self.user_email}>'

    class Meta:
        unique_together = ('reference', 'user_email')
