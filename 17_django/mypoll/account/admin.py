from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

class CustomUserAdmin(UserAdmin):
    # UserAdmin을 상속받아서 사용자 모델을 관리할 수 있는 admin 화면 설정
    list_display = ['username', 'name', 'email']
    add_fieldsets = (
        ("인증 정보", {"fields": ("username", "password1", "password2")}),
        ("개인 정보", {"fields": ("name", "email", "birthday")}),
    )
    fieldsets = (
        ("인증 정보", {"fields": ("username", "password")}),
        ("개인 정보", {"fields": ("name", "email", "birthday")}),
    )
    

admin.site.register(User, CustomUserAdmin)
