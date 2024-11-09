from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Profile, Address, VisitStatistics

from django.contrib.auth.models import Permission
admin.site.register(Permission)


class CustomUserAdmin(UserAdmin):

    fieldsets = (
        (None, {'fields': ('username','email', 'password','phone_number')}),
        ('Uprawnienia', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
             'classes': ('wide',),
             'fields': ('username','email','phone_number' ,'password1', 'password2')}
         ),
    )
    list_display = ('email', 'date_joined', 'last_login','is_staff')
    search_fields = ('username','email')
    ordering = ('username','email')


admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Address)

class VisitStatisticsAdmin(admin.ModelAdmin):
    model = VisitStatistics
    list_display = ('date', 'time', 'visited_site','ip','system','browser')
    ordering = ('-date','-time')
    search_fields = ('system','browser')
    list_filter = ('visited_site','system','browser')
    # readonly_fields = ['visited_site','ip','system','browser']
    
admin.site.register(VisitStatistics, VisitStatisticsAdmin)