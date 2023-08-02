from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import Group
from .models import User, OtpCode


@admin.register(OtpCode)
class OtoCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number', 'code', 'created',)


class UserAdmin(BaseUserAdmin):
    '''
    This class optimizes the admin panel
    '''
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('email', 'phone_number', 'is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('email', 'phone_number', 'full_name', 'password')}),
        ('Permission',
         {'fields': ('is_active', 'is_admin', 'is_superuser', 'last_login', 'groups', 'user_permissions')}),
        ('location', {'fields': ('address', 'zip_code')}),
    )

    add_fieldsets = (
        (None, {'fields': ('phone_number', 'email', 'full_name', 'address', 'zip_code', 'password1', 'password2')}),
    )

    search_field = ('email', 'full_name')
    ordering = ('full_name',)
    readonly_fields = ('last_login',)

    filter_horizontal = ('groups', 'user_permissions',)

    def get_form(self, request, obj=None, **kwargs):
        '''
        We use this method to prevent a normal user from becoming an admin in the admin panel
        '''
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled = True
        return form


admin.site.unregister(Group)
admin.site.register(User, UserAdmin)
