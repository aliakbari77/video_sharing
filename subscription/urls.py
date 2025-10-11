from django.urls import path
from subscription.views import PaymentView, SubscriptionPlansView, UnsubscribeView, VideoDetailView, VideoView, WalletTransactionView

urlpatterns = [
    path('wallet/<str:transaction_type>/', WalletTransactionView.as_view(), name='wallet-deposit'),
    path('subscription-plans/', SubscriptionPlansView.as_view(), name='subscription-plans'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('videos/', VideoView.as_view(), name='video-list'),
    path('video/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('unsubscribe/', UnsubscribeView.as_view(), name='unsubscribe'),
]