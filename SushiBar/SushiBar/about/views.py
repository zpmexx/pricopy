from django.shortcuts import render
from django.shortcuts import render,get_object_or_404
from. models import AboutUs
import datetime
from users.models import VisitStatistics
from users.statistic import visit_statistic
# Create your views here.

def about_us_view(request):
    name = 'O nas'
    visit_statistic(request,name)
    text = AboutUs.objects.all()
    if len(text)>0:
        text = text[0]
    context = {"text": text}
    return render (request,
                   'about/about_us.html',
                   context)

# def bad_request_400(request,*args, **argv):
#     pass

# def permission_denied_403(request,*args, **argv):
#     pass

# def page_not_found_404(request,*args, **argv):
#     print('witam')

# def server_error_500(request,*args, **argv):
#     pass

