# Python Imports
import uuid

# Django Imports
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField()

    def __str__(self) -> str:
        return self.user.username
    
    def update_balance(self, transaction_type, amount) -> bool:
        status = False
        if transaction_type == "borrow":
            self.balance += int(amount)
            status = True
        elif transaction_type == "lend" and self.balance >= int(amount):
            self.balance -= int(amount)
            status = True
        return status

    def change_balance(self, transactions):
        for type, amount in transactions:
            if type == "borrow":
                self.balance -= int(amount)
            elif type == "lend":
                self.balance += int(amount)
        self.save()


class Transaction(models.Model):
    transaction_status = (("unpaid", "Unpaid"), ("paid", "Paid"))
    transaction_type = (("borrow", "Borrow"), ("lend", "Lend"))
    transaction_id = models.UUIDField(unique=True, default=uuid.uuid4)
    transaction_from = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="sender"
    )
    transaction_to = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="receiver"
    )
    type = models.CharField(max_length=20, choices=transaction_type)
    date = models.DateTimeField(default=timezone.now)
    status = models.CharField(
        max_length=20, choices=transaction_status, default="unpaid"
    )
    reason = models.TextField(null=True, blank=True)
    amount = models.PositiveBigIntegerField(default=0)

    def __str__(self) -> str:
        return str(self.transaction_id)
