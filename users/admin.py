from django.contrib import admin
from users.models import User

@admin.register(User)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'password', 'token')
