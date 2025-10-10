from django.urls import path
from subscription.views import WalletTranactionView

urlpatterns = [
    path('wallet/<str:transaction_type>/', WalletTranactionView.as_view(), name='wallet-deposit'),
]