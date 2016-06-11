from django.contrib import admin

from .models import UserProfile


class UserProfileModelAdmin(admin.ModelAdmin):
    class Meta:
        model = UserProfile

admin.site.register(UserProfile, UserProfileModelAdmin)
