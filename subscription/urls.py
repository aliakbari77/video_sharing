from django.urls import path
from subscription.views import (
    PaymentHistoryView,
    PaymentView, 
    SubscriptionPlansView, 
    UnsubscribeView, 
    VideoDetailView, 
    VideoView, 
    WalletTransactionView, 
    WatchHistoryByVideoView, 
    WatchHistoryView
    )

urlpatterns = [
    path('wallet/<str:transaction_type>/', WalletTransactionView.as_view(), name='wallet-deposit'),
    path('subscription-plans/', SubscriptionPlansView.as_view(), name='subscription-plans'),
    path('payment/', PaymentView.as_view(), name='payment'),
    path('videos/', VideoView.as_view(), name='video-list'),
    path('video/<int:pk>/', VideoDetailView.as_view(), name='video-detail'),
    path('unsubscribe/', UnsubscribeView.as_view(), name='unsubscribe'),
    path('watch-history/', WatchHistoryView.as_view(), name='watch-history'),
    path('watch-history/video/<int:video_id>/', WatchHistoryByVideoView.as_view(), name='watch-history-video'),
    path('payment-history/', PaymentHistoryView.as_view(), name='payment-history')
]