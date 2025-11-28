from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Perfil'

class UserAdmin(UserAdmin):
    inlines = (ProfileInline,)

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'cargo', 'valor_hora', 'departamento', 'ativo']
    list_filter = ['cargo', 'ativo', 'departamento']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
    ordering = ['user__username']
