from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse
from .models import News, MainSiteText
import datetime
from users.models import VisitStatistics
from users.statistic import visit_statistic
# Create your views here.

def temporary_main(request):
    main_content = MainSiteText.objects.all()
    latest_three_news = News.objects.all().order_by('-date')[:3]
    context = {'main_content' : main_content,
    'latest_three_news' : latest_three_news}
    return render (request, 'news/temporary_main.html',context)

def news_list(request):
    name = 'Aktualnosci'
    visit_statistic(request,name)
    news = News.objects.all().order_by('-date')
    context = {'news' : news}
    return render (request, 'news/news_list.html',context)

def news_detail(request, slug):
    name = slug
    visit_statistic(request,name)
    news = get_object_or_404(News, slug=slug)
    context = {'news' : news}
    return render (request, 'news/news_detail.html',context)