from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.contrib import messages
from .forms import CreateConctactForm
from django.core.mail import send_mail, EmailMessage
import datetime
from users.models import VisitStatistics
from users.statistic import visit_statistic

def contactFormView(request):
    name = 'Kontakt' #nazwa strony dodawana do statystyk
    visit_statistic(request,name)
    if request.user.is_authenticated:
        form = CreateConctactForm(
            initial={'name': request.user,  # gdy uzytkownik bedzie mial first name to mozna podmienic
                     'email': request.user.email})
    else:
        form = CreateConctactForm()
    if request.method == "POST":
        form = CreateConctactForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            title = form.cleaned_data.get('title')
            content = form.cleaned_data.get('content')
            messages.success(request, f'Dziękujemy {user} za zgłoszenie, zostało ono przyjęte do realizacji. Postaramy sie na nie odpowiedzieć jak najszybciej!', extra_tags='contact')
            send_mail(f'Dziekujemy {user} za zgłoszenie!',
                      f'Dziękujemy za kontakt. Twoje zgłoszenie zostało przyjęte do realizacji oraz postaramy się odpowiedzieć jak najszybciej!\n Temat: {title}\n Treść zgłoszenia: \n {content}',
                      'sushibar@soft21.pl', [email])
            # send_mail(title, f'mail od: {email} o tresci:\n {content}', email, ['sushibar@soft21.pl'], fail_silently=False)
            emailFromClient = EmailMessage(
                subject=title,
                body=f'mail od: {email} o tresci:\n {content}',
                from_email='sushibar@soft21.pl',
                to=['sushibar@soft21.pl'],
                reply_to=[email],
            )
            emailFromClient.send()


            return redirect('contact')
    context = {'form':form}
    return render(request, 'contact/contact.html',context)

def allauthloginview(request):
    return redirect('login')