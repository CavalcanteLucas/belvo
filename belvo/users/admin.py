from django.contrib import admin

from belvo.users.models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email", "age"]


admin.site.register(User, UserAdmin)
