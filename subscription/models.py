from datetime import timedelta
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(null=True, blank=True)
    join_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - Join Date: {self.join_date}"


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __repr__(self):
        return f'{self.name}'

    def __str__(self):
        return f'{self.name}'

class Rating(models.Model):
    rate = models.FloatField(validators=[MinValueValidator(0.0), MaxValueValidator(10.0)])
    video = models.ForeignKey('Video', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'video')


class Video(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos', null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    file = models.FileField(upload_to='videos/')
    thumbnail = models.FileField(upload_to='thumbnails/')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    duration = models.DurationField(blank=True, null=True)
    rates = models.ManyToManyField(User, through=Rating)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.title}'


class SubscriptionPlan(models.Model):
    name = models.CharField(max_length=100)
    price = models.FloatField()
    duration_days = models.PositiveIntegerField(default=30)
    description = models.TextField(blank=True)

    def __str__(self):
        return f'{self.name} - {self.duration_days}'


class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.end_date:
            self.end_date = timezone.now() + timedelta(days=self.subscription_plan.duration_days)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.subscription_plan.name} - {self.user} - {self.end_date} - {self.is_active}'


class Payment(models.Model):
    class PaymentMethod(models.TextChoices):
        online = 'online', 'Online'
        wallet = 'wallet', 'Wallet'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscription_plan = models.ForeignKey(SubscriptionPlan, on_delete=models.CASCADE, null=True)
    amount = models.FloatField()
    payment_date = models.DateTimeField(auto_now_add=True)
    payment_method = models.CharField(max_length=50, 
                                      choices=PaymentMethod.choices)
    reference_id = models.CharField(max_length=100, blank=True, null=True)
    successful = models.BooleanField(default=False)


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.FloatField()

    def __str__(self):
        return f"{self.user.username} - Balance: {self.balance}"
    
    def deposit(self, amount):
        if amount <= 0:
            raise ValueError({'error': 'Amount can not be equal to or less than 0.'})
        self.balance += amount
        self.save()
        return True

    def withdraw(self, amount):
        if self.balance >= amount:
            self.balance -= amount
            self.save()
            return True
        return False


class WalletTransaction(models.Model):
    class WalletTransactionStatus(models.TextChoices):
        DEPOSIT = 'deposit', 'Deposit'
        WITHDRAW = 'withdraw', 'Withdraw'
    
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    amount = models.FloatField()
    transaction_type = models.CharField(max_length=10, choices=WalletTransactionStatus.choices)
    created_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f'{self.wallet.user.username} - {self.amount} - {self.transaction_type}'


class WatchHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='watches')
    watched_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'video')

    def __str__(self):
        return f'{self.user.username} watched {self.video.title}'


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    video = models.ForeignKey(Video, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    