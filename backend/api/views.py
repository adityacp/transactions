# Django Imports
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view, authentication_classes, permission_classes
)
from django.contrib.auth import authenticate
from django.db.models import Q
from django.db import transaction

# Local Imports
from api.models import Account, Transaction
from api.serializers import (
    AccountSerializer, TransactionSerializer, UserSerializer
)


@api_view(['POST'])
@authentication_classes(())
@permission_classes(())
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    if user is not None and user.is_authenticated:
        token, created = Token.objects.get_or_create(user=user)
        account = Account.objects.only("id", "balance").get(user_id=user.id)
        data = {
            'token': token.key, 'success': True,
            'account': AccountSerializer(
                account, context={"fields": ["id", "balance"]}
            ).data,
            'user_data': UserSerializer(
                user, context={"exclude": ["last_login", "date_joined"]}
            ).data
        }
        status_code = status.HTTP_200_OK
    else:
        data = {
            'message': 'Invalid Username/Password', 'success': False
        }
        status_code = status.HTTP_400_BAD_REQUEST
    return Response(data, status=status_code)


@api_view(["POST"])
@transaction.atomic
def add_transaction(request):
    user = request.user
    data = request.data.copy()
    transaction_amt = data.get("amount")
    sender_id = data.pop("sender_id")
    receiver_id = data.pop("receiver_id")
    data["transaction_from_id"] = sender_id
    data["transaction_to_id"] = receiver_id
    sender = Account.objects.only(
        "user_id", "balance").get(id=sender_id)
    receiver = Account.objects.only(
        "user_id", "balance").get(id=receiver_id)
    success = Account.objects.update_accounts_balance(
        sender, receiver, transaction_amt
    )
    if not success:
        msg = "Bearer has low balance"
        context = {"success": success, "message": msg}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)

    balance = (
        sender.balance if sender.user_id == user.id else receiver.balance
    )
    transaction = Transaction.objects.create(**data)
    context = {
        "transaction": TransactionSerializer(transaction).data,
        "success": True, "balance": balance
    }
    status_code = status.HTTP_201_CREATED
    return Response(context, status=status_code)


@api_view(["GET", "POST"])
def get_transactions(request):
    user = request.user
    account = Account.objects.only("id").get(user_id=user.id)
    transactions = Transaction.objects.filter(
        Q(transaction_from=account.id) | Q(transaction_to=account.id)
    )
    if request.method == "POST":
        filters = request.data.get("filters")
        if filters:
            filters = Transaction.objects.process_filters(filters)
            transactions = transactions.filter(**filters)
    context = {
        "transactions": TransactionSerializer(transactions, many=True).data,
        "success": True
    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(["POST"])
@transaction.atomic
def mark_paid(request):
    user = request.user
    data = request.data.copy()
    try:
        transaction = Transaction.objects.select_related(
            "transaction_from", "transaction_to").get(
            Q(transaction_id=data.get("transaction_id")) & Q(status="unpaid")
        )
    except Transaction.DoesNotExist:
        msg = "Amount is already paid or transaction Id does not exist"
        context = {
            "success": False, "message": msg
        }
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    sender = transaction.transaction_from
    receiver = transaction.transaction_to
    success = Account.objects.update_accounts_by_transaction(
        sender, receiver, transaction.amount, transaction.type
    )
    if success:
        transaction.status = "paid"
        transaction.save()
    else:
        msg = "Bearer account balance is low"
        context = {"success": success, "message": msg}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    balance = (
        sender.balance if sender.user_id == user.id else receiver.balance
    )
    context = {
        "transactions": TransactionSerializer(transaction).data,
        "success": True, "balance": balance
    }
    status_code = status.HTTP_201_CREATED
    return Response(context, status=status_code)


@api_view(["GET"])
def get_accounts(request):
    user = request.user
    accounts = Account.objects.exclude(user_id=user.id)
    context = {
        "accounts": AccountSerializer(
            accounts, many=True, context={"exclude": ["balance"]}
        ).data,
        "success": True
    }
    return Response(context, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_statistics(request):
    user = request.user
    account = Account.objects.only("id", "balance").get(user_id=user.id)
    transactions = Transaction.objects.filter(
        Q(transaction_from=account.id) | Q(transaction_to=account.id)
    )
    date_wise_data = Transaction.objects.get_date_wise_data(
        transactions, account.id
    )
    account_data = Transaction.objects.get_account_data(
        transactions, account.id
    )
    account_data["balance"] = account.balance
    owe_data = Transaction.objects.get_owe_count(
        transactions, account.id
    )
    return Response(
        {"date_wise_data": date_wise_data, "account_data": account_data,
         "owe_data": owe_data}
    )
