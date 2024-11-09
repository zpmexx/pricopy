from django.urls import path
from .views import register_view, account_list_view, user_detail_view, MyTokenObtainPairView
from rest_framework_simplejwt import views as jwt_views

app_name = "users"

urlpatterns = [
    path('token/obtain/', MyTokenObtainPairView.as_view(), name='token_create'),  # override sjwt stock token
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('create/', register_view, name = 'register'),
    path('<int:id>/', user_detail_view, name = 'detail'),
    path('', account_list_view, name = 'accounts')
]
