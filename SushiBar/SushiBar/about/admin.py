from django.contrib import admin
from .models import AboutUs

class AboutUsAdmin(admin.ModelAdmin):

    list_display = ('title', 'date_created',)
admin.site.register(AboutUs, AboutUsAdmin)
