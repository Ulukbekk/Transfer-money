from rest_framework.response import Response

from .permissions import IsOwner
from .serializers import AccountRegistrationSerializer, AccountDetailSerializer, TransferDetailSerializer
from .models import Account
from rest_framework import generics, permissions, status

from .services import TransferService, TopUpService
from .validators import TopUpValidator


class AccountRegisterAPIView(generics.CreateAPIView):
    """
    This endpoint registers users based on the fields
    """
    serializer_class = AccountRegistrationSerializer
    permission_classes = (permissions.AllowAny,)


class AccountDetailAPIView(generics.RetrieveAPIView):
    serializer_class = AccountDetailSerializer
    queryset = Account.objects.all()
    permission_classes = (permissions.IsAuthenticated, IsOwner)


class TransactionAPIView(generics.GenericAPIView):
    serializer_class = TransferService
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def post(self, request, pk):

        account_idn = request.POST.get('account idn')
        transfer = request.POST.get('transfer amount')
        account = Account.objects.filter(id=pk).first()
        recipient = Account.objects.filter(idn=account_idn).first()

        print(request.user, account.username)
        if request.user != account.user:
            return Response('Error', status=status.HTTP_405_METHOD_NOT_ALLOWED)
        elif account.balance < float(transfer):
            return Response('Insufficient funds', status=status.HTTP_412_PRECONDITION_FAILED)
        self.serializer_class.transfer(account.user, recipient.user, transfer)
        account = Account.objects.filter(id=pk).first()
        serializer = TransferDetailSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BalanceIncreaseAPIView(generics.GenericAPIView):
    validator_class = TopUpValidator
    service_class = TopUpService

    def post(self, request, *args, **kwargs):
        balance = request.data.get('balance')
        if not self.validator_class.validate_balance(balance):
            return Response('Pass balance to top up', status=status.HTTP_400_BAD_REQUEST)

        self.service_class.top_up(request.user, balance)

        return Response('Ok', status=status.HTTP_200_OK)