from django.contrib import admin
from .models import BarInformations, OpeningHours, ContactModel, RealizationHours, RealizationStatus
# Register your models here.


class OpeningHoursAdmin(admin.ModelAdmin):
    model = OpeningHours
    list_display = ['weekday','from_hour','to_hour']
    ordering = ['weekday']

class ContactModelAdmin(admin.ModelAdmin):
    model = OpeningHours
    list_display = ['status','name','email','date']
    ordering = ['status','date']

class RealizationHoursAdmin(admin.ModelAdmin):
    model = OpeningHours
    list_display = ['weekday','from_hour','to_hour']
    ordering = ['weekday']

admin.site.register(BarInformations)
admin.site.register(OpeningHours, OpeningHoursAdmin)
admin.site.register(ContactModel,ContactModelAdmin)
admin.site.register(RealizationHours,RealizationHoursAdmin)
admin.site.register(RealizationStatus)