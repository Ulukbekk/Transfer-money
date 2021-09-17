from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.response import Response

from users.models import Account
from django.db import transaction


class TransferService:

    @classmethod
    @transaction.atomic
    def transfer(cls, user: User, reception: User, transfer: float) -> None:
        account = Account.objects.select_for_update().filter(user=user).first()
        reception = Account.objects.select_for_update().filter(user=reception).first()
        with transaction.atomic():
            if account.balance >= float(transfer):
                account.balance -=float(transfer)
                account.save()

                reception.balance += float(transfer)
                reception.save()


class TopUpService:

    @classmethod
    def top_up(cls, user: User, balance: float) -> None:
        account = Account.objects.filter(user=user).first()
        account.balance += float(balance)
        account.save()