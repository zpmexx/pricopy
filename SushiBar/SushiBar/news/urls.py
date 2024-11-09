from django.contrib import admin
from django.urls import path, include
from. import views

app_name = "news"

urlpatterns = [
    path('aktualnosci/' ,views.news_list, name="home"),
    path('' ,views.temporary_main, name="temporary_main"),

    path('aktualnosci/<slug:slug>/', views.news_detail, name='detail'),
]
