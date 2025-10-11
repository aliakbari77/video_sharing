from django.contrib import admin
from subscription.models import SubscriptionPlan, Video, Category

class SubscriptionPlanAdmin(admin.ModelAdmin):
    pass


class VideoAdmin(admin.ModelAdmin):
    pass


class CategoryAdmin(admin.ModelAdmin):
    pass

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
admin.site.register(Video, VideoAdmin)
admin.site.register(Category, CategoryAdmin)