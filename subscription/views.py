from django.contrib.auth.models import User

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from subscription.serializers import RegisterSerializer, SubscriptionPlanSerializer, WalletTransactionSerializer
from subscription.models import WalletTransaction, Wallet, SubscriptionPlan

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class WalletTranactionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, transaction_type, *args, **kwargs):
        serializer = WalletTransactionSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                wallet = Wallet.objects.get(user=request.user)
            except:
                raise NotFound({'error': f'wallet not found for {request.user.username}'})
        
        amount = float(serializer.data.get('amount'))
        
        transaction_choices = WalletTransaction.WalletTransactionStatus
        if transaction_type == transaction_choices.DEPOSIT:
            wallet.deposit(amount)
        elif transaction_type == transaction_choices.WITHDRAW:
            wallet.withdraw(amount)
        else:
             raise APIException({'error': 'Transaction not found.'})

        return Response(data={'balance': wallet.balance}, status=status.HTTP_200_OK)


class SubscriptionPlansView(ListAPIView):
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer