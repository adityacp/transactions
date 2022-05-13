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
from django.utils import timezone

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
    transaction_type = data.get("type")
    transaction_amt = data.get("amount")
    data["transaction_from_id"] = data.pop("transaction_from")
    data["transaction_to_id"] = data.pop("transaction_to")
    account = Account.objects.only("balance").get(user_id=user.id)
    update_status = account.update_balance(transaction_type, transaction_amt)
    if not update_status:
        context = {"success": update_status, "message": "You have low balance"}
        return Response(context, status=status.HTTP_400_BAD_REQUEST)
    account.save()
    transaction = Transaction.objects.create(**data)
    context = {
        "transaction": TransactionSerializer(transaction).data,
        "success": True, "balance": account.balance
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
    transactions = Transaction.objects.filter(
        transaction_id__in=data.get("transaction_ids")
    )
    for transaction in transactions:
        transaction.status = "paid"
    account = Account.objects.only("id").get(user_id=user.id)
    Transaction.objects.bulk_update(transactions, ['status'])
    account.change_balance(transactions.values_list("type", "amount"))
    context = {
        "transactions": TransactionSerializer(transactions, many=True).data,
        "success": True, "balance": account.balance
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

