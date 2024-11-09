from django.shortcuts import render, redirect 
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterUserForm, UpdateProfileForm, UpdateUserForm, UpdateAddressForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Address
from menu.models import Order,Cart,Cart_item,Product
import datetime
from .models import VisitStatistics
from users.models import VisitStatistics
from .statistic import visit_statistic
from SushiBar.settings import EMAIL_HOST_USER, P24
import json
from menu.payment import Przelewy24
from django.core.mail import send_mail

import allauth.socialaccount.providers as ASP

# Create your views here.

def registerPage(request):
    name = 'Rejestracja'
    visit_statistic(request,name)
    form = RegisterUserForm()
    if request.method == "POST":
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request,'Stworzono konto dla ' + user, extra_tags='singup')
            return redirect('login')
        else:
            messages.error(request,'Błąd tworzenia konta ', extra_tags='singup')

    context = {'form':form}
    return render (request, 'users/register.html',context)

def loginPage(request):
    name = 'Logowanie'
    visit_statistic(request,name)
    if request.user.is_authenticated:
        return redirect('main')
    else:
        if request.method == "POST":
            username = request.POST.get('uname')
            password = request.POST.get('psw')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if request.GET.get('next') is not None:
                    return redirect(request.GET.get('next'))
                return redirect('main')
            else:
                messages.info(request, 'Niepoprawne dane logowania', extra_tags='bad_credentials')
        context = {}
        return render(request, 'users/login.html', context)

def logoutPage(request):
    logout(request)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def profile(request):
    name = 'Profil'
    visit_statistic(request,name)
    user_form = UpdateUserForm(instance=request.user)
    profile_form = UpdateProfileForm(instance=request.user.profile)
    user_orders = Order.objects.filter(user=request.user)
    try:
        user_address = Address.objects.get(user=request.user)
    except Address.DoesNotExist:
        user_address = False

    if not user_address:
        address_form = UpdateAddressForm()
    else:
        address_form = UpdateAddressForm(instance=user_address)

    if request.method == "POST":
        address_form = UpdateAddressForm(request.POST)
        user_form = UpdateUserForm(request.POST, instance = request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES,instance = request.user.profile)
        if user_form.is_valid() and profile_form.is_valid() and address_form.is_valid():
            try:
                user_address = Address.objects.get(user=request.user)
            except Address.DoesNotExist:
                user_address = False

            if not user_address:
                user_address = Address.objects.create(city = address_form.cleaned_data['city'], house_number = address_form.cleaned_data['house_number'],
                                                      flat_number = address_form.cleaned_data['flat_number'], street = address_form.cleaned_data['street'],
                                                      postal_code = address_form.cleaned_data['postal_code'], user = request.user)

            address_form = UpdateAddressForm(request.POST, instance=user_address)

            address_form.save()
            user_form.save()
            profile_form.save()
            messages.success(request,'Zaaktualizowano dane.', extra_tags='update')
            return redirect('profile')
        else:
            messages.warning(request,'Użytkownik o tych danych znajduje się w systemie!', extra_tags='warn')
            # return redirect('profile')

        
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'address_form': address_form,
        'user_orders': user_orders,
    }
    return render(request, 'users/profile.html',context)


@login_required
def ordersPage(request):

    if request.method == "GET" and len(request.GET.get('sessionId','')):
        sessionId = request.GET.get('sessionId','')
        print(sessionId)
        result = json.loads(Przelewy24.getPaymentInfo(sessionId)) #status=0 - płatność nieudana, 1-nie potwierdzona przez nas (lub nieprwaidłowa kwota), 2-poprawna płatność
        # print(result)
        try:
            if "error" in result:
                print("home error: ", result)
                messages.error(request, f'Błąd płatności')
                return redirect('zamowienia')
            elif "data" in result:
                result = result["data"]
                print("home result: ",result)

                order = Order.objects.get(sessionId=sessionId)
                order.paymentOrderId = result["orderId"]
                order.payment_status = result["status"]
                order.save()
                #print(vars(order))
                #print(order.phone_number)
                result = Przelewy24.confirmPayment(order)
                if "error" in result:
                    # print("home error: ", result)
                    messages.error(request, f'Błąd płatności')
                    return redirect('zamowienia')
                else:
                    result = json.loads(Przelewy24.getPaymentInfo(sessionId)) #status=0 - płatność nieudana, 1-nie potwierdzona przez nas (lub nieprwaidłowa kwota), 2-poprawna płatność
                    # print(result)
                    try:
                        if "error" in result:
                            # print("home error: ", result)
                            messages.error(request, f'Błąd płatności')
                            return redirect('zamowienia')
                        elif "data" in result:
                            result = result["data"]
                            # print("home result: ",result)
                            order = Order.objects.get(sessionId=sessionId)
                            if order.status == 1:
                                order.status = 2
                            order.payment_status = result["status"]
                            order.save()
                            return redirect('zamowienia')
                    except:
                        pass
        except:
                messages.error(request, f'Błąd płatności')
                return redirect('zamowienia')

    not_confirmed_orders = Order.objects.filter(user=request.user, status=1)
    for order in not_confirmed_orders:
        if order.payment_status != 2:
            checkPaymentConfirm(order)

    user_orders = Order.objects.filter(user=request.user).order_by('-created')

    context = {
        'user_orders': user_orders
    }
    return render(request, 'users/orders.html', context)

@login_required
def orderPage(request, orderId):
    user_order = Order.objects.filter(user=request.user, orderId=orderId).first()
    if request.method == "POST":
        if request.POST.get("payagain"):
            user_order.generateSessionId()
            user_order.save()
            p24respon = json.loads(Przelewy24.registerPayment(user_order, user_order.user.email))

            messages.success(request, f'Zamówienie zostało złożone! Informacje na mailu!', extra_tags='order_completed')
            send_mail(f'Twoje zamówienie zostało zatwierdzone!',
                      f'Zamówienie zostało złożone! Szacowany czas dostawy: 45 minut!',
                      EMAIL_HOST_USER, [user_order.user.email])
            send_mail(f'Nowe zamówienie od użytkownika {request.user.username}',
                      f'Użytkownik {request.user.username} złożył zamówienie. Szczegóły w panelu.',
                      EMAIL_HOST_USER, [EMAIL_HOST_USER])

            try:
                if "error" in p24respon:
                    print(p24respon)
                    messages.error(request, f'Błąd płatności')
                elif "data" in p24respon:
                    result = p24respon["data"]
                    print(result)
                    print(p24respon["data"]["token"])
                    return redirect(P24['trnRequest'] + str(p24respon["data"]["token"]))
            except:
                messages.error(request, f'Błąd płatności')
        elif request.POST.get("cancelorder"):
            user_order.status = 5
            user_order.save()


    if user_order.status == 1 and user_order.payment_status != 2:
        user_order = checkPaymentConfirm(user_order)

    context = {
        'user_order': user_order
    }
    return render(request, 'users/order.html', context)

def checkPaymentConfirm(user_order):
    # print(sessionId)
    sessionId = user_order.sessionId
    result = json.loads(Przelewy24.getPaymentInfo(sessionId))  # status=0 - płatność nieudana, 1-nie potwierdzona przez nas (lub nieprwaidłowa kwota), 2-poprawna płatność
    # print(result)
    try:
        if "error" not in result and "data" in result:
            result = result["data"]
            # print("home result: ",result)
            user_order.paymentOrderId = result["orderId"]
            user_order.payment_status = result["status"]
            user_order.save()
            # print(vars(order))
            # print(order.phone_number)
            result = Przelewy24.confirmPayment(user_order)
            if "error" not in result:
                result = json.loads(Przelewy24.getPaymentInfo(sessionId))  # status=0 - płatność nieudana, 1-nie potwierdzona przez nas (lub nieprwaidłowa kwota), 2-poprawna płatność
                # print(result)
                try:
                    if "error" not in result and "data" in result:
                        result = result["data"]
                        # print("home result: ",result)
                        if user_order.status == 1:
                            user_order.status = 2
                        user_order.payment_status = result["status"]
                        user_order.save()
                except:
                    pass
    except:
        pass

    return user_order

