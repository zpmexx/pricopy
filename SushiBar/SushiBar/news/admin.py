from django.contrib import admin
from .models import News, MainSiteText
# Register your models here.

class NewsAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    model = News
    list_display = ['title','date']
    search_fields = ['title']
    ordering = ['-date','title']


admin.site.register(News, NewsAdmin)
admin.site.register(MainSiteText)