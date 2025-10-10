from django.urls import path
from subscription.views import WalletDeposit

urlpatterns = [
    path('wallet/deposit/', WalletDeposit.as_view(), name='wallet-deposit'),
]