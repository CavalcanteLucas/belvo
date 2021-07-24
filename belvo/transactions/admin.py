from django.contrib import admin

from belvo.transactions.models import Transaction


class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "reference",
        "account",
        "amount",
        "type",
        "category",
        "user_id",
        "date",
    ]


admin.site.register(Transaction, TransactionAdmin)
