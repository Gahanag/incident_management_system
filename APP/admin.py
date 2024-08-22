from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
    list_display = ["id","email", "Reporter_Name", "is_admin"]
    list_filter = ["is_admin"]

    fieldsets = [
        ('User_credentials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["Reporter_Name","phone_number","Address", "Pin_code" ]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]

    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "Reporter_Name" ,"phone_number","Address","Pin_code","City","Country", "password1", "password2"],
            },
        ),
    ]

    search_fields = ["email"]
    ordering = ["email",'id']
    filter_horizontal = []

admin.site.register(User, UserAdmin)

admin.site.register(Incident)