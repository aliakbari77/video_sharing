from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.models import User

from decimal import Decimal

from subscription.models import Payment, Subscription, Wallet, Profile, WalletTransaction


@receiver(post_save, sender=User)
def create_wallet(sender, instance, created, **kwargs):
    if created:
        Wallet.objects.create(user=instance, balance=0)
    
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(pre_save, sender=Wallet)
def track_wallet_balance_change(sender, instance, **kwargs):
    if not instance.pk:
        instance._old_balance = Decimal('0.00')
    else:
        old_balance = Wallet.objects.get(pk=instance.pk).balance
        instance._old_balance = old_balance

@receiver(post_save, sender=Wallet)
def create_wallet_transaction(sender, instance, **kwargs):
    difference = instance.balance - instance._old_balance
    
    if difference == 0:
        return
    
    if difference > 0:
        transaction_type = 'deposit'
    else:
        transaction_type = 'withdraw'
    
    WalletTransaction.objects.create(
        wallet=instance,
        amount=difference,
        transaction_type=transaction_type
    )

@receiver(post_save, sender=Payment)
def create_subscription(sender, instance, created, **kwargs):
    if created:
        Subscription.objects.create(
            user=instance.user,
            subscription_plan=instance.subscription_plan,
            is_active=True
        )