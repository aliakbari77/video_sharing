from django.contrib import admin
from subscription.models import SubscriptionPlan, Video, Category, Wallet, Subscription

class SubscriptionPlanAdmin(admin.ModelAdmin):
    pass


class VideoAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass


class WalletAdmin(admin.ModelAdmin):
    pass


class SubscriptionAdmin(admin.ModelAdmin):
    pass


admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Wallet, WalletAdmin)
admin.site.register(Subscription, SubscriptionAdmin)