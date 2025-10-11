from django.contrib.auth.models import User
from rest_framework import serializers

from subscription.models import Payment, SubscriptionPlan, Video

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


class UnsubscribeSerializer(serializers.Serializer):
    subscription_id = serializers.IntegerField()