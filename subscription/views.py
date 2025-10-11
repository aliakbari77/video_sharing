from django.contrib.auth.models import User

from rest_framework.views import APIView
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException

from subscription.permissions import CanWatchVideo
from subscription.serializers import (
    PaymentSerializer, 
    RegisterSerializer, 
    SubscriptionPlanSerializer, 
    UnsubscribeSerializer, 
    VideoDetailSerializer, 
    VideoListSerializer, 
    WalletTransactionSerializer,
    WatchHistorySerializer
    )
from subscription.models import (
    Payment, 
    Subscription, 
    Video, 
    WalletTransaction, 
    Wallet, 
    SubscriptionPlan,
    WatchHistory,
    )


class RegisterView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]


class WalletTransactionView(CreateAPIView):
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
                

class VideoView(ListAPIView):
    queryset = Video.objects.all()
    serializer_class = VideoListSerializer
    permission_classes = [AllowAny]


class VideoDetailView(APIView):
    permission_classes = [IsAuthenticated, CanWatchVideo]

    def get(self, request, *args, **kwargs):
        video_id = self.kwargs.get('pk')
        try:
            video = Video.objects.get(id=video_id)
        except:
            raise NotFound({'error': 'Video not found.'})
        
        user = request.user
        if not WatchHistory.objects.filter(user=user, video=video).exists():
            WatchHistory.objects.create(user=user, video=video)
        
        serializer = VideoDetailSerializer(video)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UnsubscribeView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = UnsubscribeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                subscription = Subscription.objects.get(id=serializer.data.get('subscription_id'),
                                                        user=request.user, 
                                                        is_active=True)
                subscription.is_active = False
                subscription.save()
                return Response(data={'message': 'The unsubscribe action successfully.'},
                                status=status.HTTP_200_OK)
            except:
                raise NotFound({'error': 'The active subscription not found.'})
        return Response(data={'error': 'Please send the subscription.'})
    

class WatchHistoryView(ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = WatchHistory.objects.all()
    serializer_class = WatchHistorySerializer


class WatchHistoryByVideoView(APIView):

    def get(self, request, video_id, *args, **kwargs):
        try:
            video = Video.objects.get(id=video_id)
        except:
            raise NotFound({'error': 'Video not found.'})
        
        watch_history = WatchHistory.objects.filter(video=video)

        serializer = WatchHistorySerializer(watch_history, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
        
