from django.contrib import admin
from django.urls import path
from. import views

app_name = "menu"

urlpatterns = [
    path('' ,views.home, name="home"),
    path('product_quantity_decrease/<slug:slug>' ,views.product_quantity_decrease, name="product_quantity_decrease"),
    path('product_quantity_increase/<slug:slug>' ,views.product_quantity_increase, name="product_quantity_increase"),
    path('add_to_cart/<slug:slug>' ,views.add_to_cart, name="add_to_cart"),
    path('add_to_cart/<slug:slug>/<quantity>', views.add_to_cart, name="add_to_cart"),
    path('delete_from_cart/<slug:slug>' ,views.delete_from_cart, name="delete_from_cart"),
    path('<slug:slug>/', views.detail, name='product_detail'),
]