from django.urls import path
from .views import GetNewsSerializer
from .views import get_news,create_news, news_detail
app_name = "news"

urlpatterns = [
    path('', get_news, name = 'get_news'),
    path('create/', create_news, name = 'create_news'),
    path('<slug:slug>/', news_detail, name = 'news_detail'),
]
