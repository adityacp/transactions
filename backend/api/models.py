# Python Imports
import uuid
import pandas as pd
from datetime import datetime

# Django Imports
from django.db import models
from django.contrib.auth.models import User


class AccountManager(models.Manager):

    def update_accounts_balance(self, sender, receiver, amount):
        status = sender.can_debit_amount(amount)
        if status:
            sender.update_balance("lend", amount)
            receiver.update_balance("borrow", amount)
        return status

    def update_accounts_by_transaction(self, sender, receiver, amount, type):
        status = False
        if type == "lend":
            if receiver.can_debit_amount(amount):
                sender.update_balance("borrow", amount)
                receiver.update_balance("lend", amount)
                status = True
        else:
            if sender.can_debit_amount(amount):
                sender.update_balance("lend", amount)
                receiver.update_balance("borrow", amount)
                status = True
        return status


class Account(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.PositiveIntegerField()

    objects = AccountManager()

    def __str__(self) -> str:
        return self.user.username

    def update_balance(self, transaction_type, amount) -> bool:
        if transaction_type == "borrow":
            self.balance += int(amount)
        elif transaction_type == "lend":
            self.balance -= int(amount)
        self.save()

    def can_debit_amount(self, amount):
        return self.balance > int(amount)


class TransactionsManager(models.Manager):

    def get_date_wise_data(self, transactions, account_id) -> dict:
        transactions = transactions.values(
            "created_on__date", "transaction_from_id", "transaction_to_id"
        )
        data = {"dates": [], "debits": [], "credits": []}
        if transactions.exists():
            df = pd.DataFrame(transactions)
            df1 = df.groupby(
                ["created_on__date"], as_index=False
            ).value_counts()
            data["dates"] = df["created_on__date"].unique()
            data["debits"] = df1[df1["transaction_from_id"]
                                 == account_id]["count"].to_list()
            data["credits"] = df1[df1["transaction_to_id"]
                                  == account_id]["count"].to_list()
        return data

    def get_account_data(self, transactions, account_id) -> dict:
        transactions = transactions.values(
            "transaction_from_id", "transaction_to_id", "amount"
        )
        data = {"total_debt": None, "total_lend": None}
        if transactions.exists():
            df = pd.DataFrame(transactions)
            data["total_debt"] = df[df["transaction_to_id"] 
                                    == account_id]["amount"].sum()
            data["total_lend"] = df[df["transaction_from_id"]
                                    == account_id]["amount"].sum()
        return data

    def get_owe_count(self, transactions, account_id):
        transactions = transactions.values(
            "transaction_from_id", "transaction_to_id"
        )
        data = {"owe_me": None, "owe_others": None}
        if transactions.exists():
            data["owe_me"] = transactions.filter(
                transaction_from_id=account_id
            ).count()
            data["owe_others"] = transactions.filter(
                transaction_to_id=account_id
            ).count()
        return data

    def process_filters(self, filters):
        if "date" in filters:
            start_date, end_date = filters.pop("date")
            filters["created_on__gte"] = datetime.strptime(
                start_date, '%d-%m-%Y')
            filters["created_on__lte"] = datetime.strptime(
                end_date, '%d-%m-%Y')
        return filters


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
    status = models.CharField(
        max_length=20, choices=transaction_status, default="unpaid"
    )
    reason = models.TextField(null=True, blank=True)
    amount = models.PositiveBigIntegerField(default=0)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    objects = TransactionsManager()

    def __str__(self) -> str:
        return str(self.transaction_id)
