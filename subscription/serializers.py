from django.contrib.auth.models import User
from rest_framework import serializers

from subscription.models import Payment, SubscriptionPlan, Video, WatchHistory, Comment

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    password2 = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']

    def validate(self, attrs):
        if attrs.get('password') != attrs.get('password2'):
            raise serializers.ValidationError({'password': 'Password do not match.'})
        return attrs
    
    def create(self, validated_data):
        validated_data.pop('password2')
        user = User.objects.create_user(**validated_data)
        return user
    

class WalletTransactionSerializer(serializers.Serializer):
    amount = serializers.FloatField()


class SubscriptionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubscriptionPlan
        fields = '__all__'


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['subscription_plan', 
                  'payment_method']
        

class VideoListSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name') # TODO: if has multiple category change here.

    class Meta:
        model = Video
        fields = ['id',
                  'title',
                  'category',
                  'description']
        

class VideoDetailSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source='category.name') # TODO: if has multiple category change here.

    class Meta:
        model = Video
        fields = '__all__'


class UnSubscribeSerializer(serializers.Serializer):
    subscription_id = serializers.IntegerField()


class WatchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchHistory
        fields = '__all__'


class PaymentHistorySerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username')
    subscription_plan = serializers.CharField(source='subscription_plan.name')
    class Meta:
        model = Payment
        fields = '__all__'


class RenewalSubscribeSerializer(serializers.Serializer):
    subscription_id = serializers.IntegerField()
    payment_method = serializers.CharField()


class CommentSerializer(serializers.ModelSerializer):
    video_id = serializers.IntegerField()

    class Meta:
        model = Comment
        fields = ['video_id', 'content']