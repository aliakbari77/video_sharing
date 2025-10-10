from django.urls import path
from subscription.views import PaymentView, SubscriptionPlansView, WalletTranactionView

urlpatterns = [
    path('wallet/<str:transaction_type>/', WalletTranactionView.as_view(), name='wallet-deposit'),
    path('subscription-plans/', SubscriptionPlansView.as_view(), name='subscription-plans'),
    path('payment/', PaymentView.as_view(), name='payment'),
]