from django.contrib.auth.models import User

from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from subscription.serializers import PaymentSerializer, RegisterSerializer, SubscriptionPlanSerializer, WalletTransactionSerializer
from subscription.models import Payment, WalletTransaction, Wallet, SubscriptionPlan

class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class WalletTranactionView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WalletTransactionSerializer

    def post(self, request, transaction_type, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        
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
    permission_classes = [AllowAny]
    queryset = SubscriptionPlan.objects.all()
    serializer_class = SubscriptionPlanSerializer


class PaymentView(CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PaymentSerializer

    def post(self, request, *args, **kwargs):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            payment_methods = Payment.PaymentMethod
            payment_method = serializer.data.get('payment_method') 
            if payment_method == payment_methods.wallet:
                wallet = Wallet.objects.get(user=user)
                try:
                    subscription_plan_id = serializer.data.get('subscription_plan')
                    subscription_plan = SubscriptionPlan.objects.get(pk=subscription_plan_id)
                except:
                    raise NotFound({'error': 'Subscription Plan not found.'})
                amount = subscription_plan.price
                if wallet.balance >= amount:
                    Payment.objects.create(user=user, 
                                           subscription_plan=subscription_plan,
                                           amount=amount)
                    wallet.withdraw(amount)
                    return Response(data={'message': f'{user} buy {subscription_plan.name} plan successfully.'}, 
                                    status=status.HTTP_200_OK)
                else:
                    return Response({'message': 'The balance of wallet'
                                    ' is less than the price of this plan. '
                                    'Plaeas Charge the wallet and try again.'}, status=status.HTTP_200_OK)
            elif payment_method == payment_methods.online:
                return Response({'message': 'The online method is not implemented yet.'}, status=status.HTTP_200_OK)
                