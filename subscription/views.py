from django.contrib.auth.models import User

from rest_framework.generics import CreateAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status

from subscription.serializers import RegisterSerializer, WalletTransactionSerializer
from subscription.models import WalletTransaction, Wallet

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class WalletDeposit(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = WalletTransactionSerializer(data=request.data)
        if serializer.is_valid():
            try:
                wallet = Wallet.objects.get(user=request.user)
            except:
                raise NotFound({'error': f'wallet not found for {request.user.username}'})
        
        wallet = Wallet.objects.get(user=request.user)
        amount = float(serializer.data.get('amount'))
        wallet.deposit(amount)

        return Response(data={'balance': wallet.balance}, status=status.HTTP_200_OK)
