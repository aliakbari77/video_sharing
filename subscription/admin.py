from django.contrib import admin
from subscription.models import SubscriptionPlan

class SubscriptionPlanAdmin(admin.ModelAdmin):
    pass

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)