# from django.contrib import admin
# from django.contrib.auth.admin import UserAdmin
# from django.contrib.auth.models import User
# from .models import Notice

# # 기본 관리자 사이트 제목 변경
# admin.site.site_header = "Economia 관리자"
# admin.site.site_title = "Economia 관리자 포털"
# admin.site.index_title = "Economia 관리자에 오신 것을 환영합니다"

# # User 모델에 대한 관리자 인터페이스 커스터마이즈
# class CustomUserAdmin(UserAdmin):
#     list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'last_login')
#     list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
#     search_fields = ('username', 'first_name', 'last_name', 'email')
#     ordering = ('-date_joined',)

# # 기존 UserAdmin을 커스텀 버전으로 교체
# 기존 UserAdmin을 커스텀 버전으로 교체
# admin.site.unregister(User)
# admin.site.register(User, CustomUserAdmin)

# # 다른 모델들에 대한 관리자 설정
# # 예: from .models import YourModel
# # admin.site.register(YourModel)

# admin.site.register(Notice)