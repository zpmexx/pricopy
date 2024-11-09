from django.shortcuts import render,get_object_or_404,redirect 
from .models import Product,Category,Rating,Comment, Cart, Cart_item, Order, OrderItem
from .forms import RatingForm, CommentForm, OrderCreationForm, AddressOrderForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from SushiBar.settings import EMAIL_HOST_USER, P24
from users.models import Address
from django.urls import reverse
import json
import datetime
from django.utils import timezone
from contact.models import RealizationStatus,RealizationHours
from .payment import Przelewy24
from users.models import VisitStatistics
from users.statistic import visit_statistic
from contact.models import BarInformations
# Create your views here.


def home(request):
    name = 'Menu'
    visit_statistic(request,name)
    if request.user.is_authenticated:
        if request.COOKIES.get('product_before_login') is None:
            pass
        else:
            response = redirect(('main'))
            cart = Cart.objects.get(user=request.user)
            product = Product.objects.get(slug=request.COOKIES.get('product_before_login'))
            quantity = request.COOKIES.get('product_bef_login_quantity')
            # print('ilosc',quantity)
            order_item = Cart_item.objects.filter(cart = cart, product = product)
            if order_item.exists():
                item = Cart_item.objects.get(cart = cart, product = product)
                item.quantity += int(quantity)
                item.save()
            else:
                cart_item = Cart_item(product = product, cart = cart,quantity = quantity)
                cart_item.save()
            response.delete_cookie('product_before_login')
            response.delete_cookie('product_bef_login_quantity')
            return response
    categories = Category.objects.all()
    products = Product.objects.all()
    context = {
        'categories': categories,
        'products': products,
    }
    user_cart = None

    if request.user.is_authenticated:
        try:
            user_cart = Cart.objects.get(user=request.user)
            user_items = Cart_item.objects.filter(cart=user_cart)
            if len(user_items) == 0:
                user_items = 0
        except:
            user_items = 0
        context['user_items'] = user_items
        context['user_cart'] = user_cart

    return render(request, 'menu/home.html', context)

def detail(request,slug):
    product = get_object_or_404(Product, slug=slug)
    ratings = Rating.objects.filter(product=product)
    comments = Comment.objects.filter(product=product)
    rated_users = []
    if request.user.is_authenticated:
        try:
            user_vote = Rating.objects.get(product = product, user=request.user)
        except Rating.DoesNotExist:
            user_vote = None
    for rate in ratings:
        rated_users.append(rate.user)
    if request.user.is_authenticated:
        rating_form = RatingForm()
        comment_form = CommentForm()
        if request.method == "POST":
            if 'rating_form_submit' in request.POST:
                rating_form = RatingForm(request.POST)
                if rating_form.is_valid():
                    value = rating_form.cleaned_data.get('value')
                    rate = Rating(product = product, user = request.user, value = value) 
                    rate.save()
                    return HttpResponseRedirect('.')#ajax zamiast odwieżenia w przyszłości
            elif 'comment_form_submit' in request.POST:
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    content = comment_form.cleaned_data.get('content')
                    data = {
                    'product': product,
                    'user': request.user,
                    'content': content
                    }
                    comment = Comment(product = product, user = request.user, content = content) 
                    comment.save()
                    return HttpResponseRedirect('.')#ajax zamiast odwieżenia w przyszłości
        context = {'product' : product, 'rating_form': rating_form, 'ratings':ratings, 'rated_users': rated_users,'comments': comments,'user_vote': user_vote, 'comment_form': comment_form}
    else:
        context = {'product': product}

    return render(request, 'menu/product_detail.html',context)

@login_required
def user_cart_view(request):
    object = VisitStatistics.objects.all().first()
    # print(object.time)
    # print(datetime.datetime.now().time())
    # later = datetime.datetime.now().time() + datetime.timedelta(minutes=15)
    # print(later)
    order_form = OrderCreationForm()
    phone_number = request.user.phone_number
    realization_hours = RealizationHours.objects.all()
    realization_status = RealizationStatus.objects.all().first()
    today_date = timezone.now() # dziejsza data
    today_day = datetime.datetime.now().weekday() # dzisiejszy dzień
    today_realization_date = RealizationHours.objects.filter(weekday = today_day).first() # dzień z realizacji godzin
    final_realization_status = 1 #1 - mozliwosc zamawiania, 2 -brak
    final_realization_message = '' #wiadomośc zwrotna

    if realization_status == None:
        final_realization_status = 1
        final_realization_message = 'Brak danych o statusie, ale można zmawiać'
    elif realization_status.status == 3:
        final_realization_status = 2
        final_realization_message = 'Brak możliwści zamawiania do odwołania'
    elif realization_status.status == 2:
        if realization_status.from_date <= today_date <= realization_status.to_date:
            final_realization_status = 2 #brak możliwści zamawiania
            final_realization_message = realization_status.message
            print("niemoznosc realziacji zamowien ze wzgledu na status i date")
        else:
            final_realization_status = 1
            final_realization_message = 'Mimo statusu zamkneitego mozna zamawiac'
    else:
        if today_realization_date == None:
            final_realization_status = 2
            final_realization_message = 'Nie można zamawiać ponieważ na dzień dzisiejszy nie są skonfigurowane godziny realizacji zamówień'
        elif today_realization_date.status == 2:
            final_realization_status = 2
            final_realization_message = 'Nie można zamawiać ze względu na zamkniętą restaruacje dzisiaj'
        elif today_realization_date.from_hour <= today_date.time() <= today_realization_date.to_hour:
            final_realization_status = 1
            final_realization_message = 'Można zamawiać!'
        else:
            final_realization_status = 2
            final_realization_message = 'Obecnie dokonywanie zamówień jest niemożliwe, zapraszamy w godzinach pracy.'
            print('niemoznosc wyonwania zamowien ze wzgledu na godziny otawrcia')

    #potrzeba jeszcze godzin i minut z dzisiaj, godzin i minut z realization poczatek i koniec i porówntwać, dodać tez status.
    try:
        user_address = Address.objects.get(user=request.user)
    except Address.DoesNotExist:
        user_address = False
    
    if not user_address:
        address_form = AddressOrderForm(initial={'phone_number': phone_number})
    else:
        address_form = AddressOrderForm(instance=user_address, initial={'phone_number': phone_number})
    if request.method == "POST":
        if request.POST.get("clearcart"):
            cart_products = Cart_item.objects.filter(cart=Cart.objects.get(user=request.user))
            cart_products.delete()
            messages.success(request,f'Pomyślnie wyczyszczono koszyk!', extra_tags='user_cart_clear_completed')
            return redirect('menu:home')

        email = request.user.email
        if email != "":
            cart = Cart.objects.get(user=request.user)
            order_form = OrderCreationForm(request.POST)
            address_form = AddressOrderForm(request.POST)
            if order_form.is_valid() and address_form.is_valid():

                order_payment = order_form.cleaned_data['choice']
                user_comments = order_form.cleaned_data['comments']
                phone_number_given = address_form.cleaned_data['phone_number']
                total_price = 0
                try:
                    user_address = Address.objects.get(user=request.user)
                except Address.DoesNotExist:
                    user_address = False

                if not user_address:
                    user_address = Address.objects.create(city = address_form.cleaned_data['city'], house_number = address_form.cleaned_data['house_number'],
                    flat_number = address_form.cleaned_data['flat_number'], street = address_form.cleaned_data['street'],
                    postal_code = address_form.cleaned_data['postal_code'], user_first_last_name = address_form.cleaned_data['user_first_last_name'], user = request.user)

                address_form = AddressOrderForm(request.POST, instance=user_address)
                address_form.save()
                city = address_form.cleaned_data['city']
                house_number = address_form.cleaned_data['house_number']
                flat_number = address_form.cleaned_data['flat_number']
                street = address_form.cleaned_data['street']
                postal_code = address_form.cleaned_data['postal_code']
                user_first_last_name = address_form.cleaned_data['user_first_last_name']

                cart_products = Cart_item.objects.filter(cart=Cart.objects.get(user=request.user))
                for item in cart_products:
                    if item.product.is_promoted() == True:
                        total_price += item.product.promotion_price * item.quantity
                    else:
                        total_price += item.product.price * item.quantity
                total_price += BarInformations.objects.all().first().delivery_cost
                order = Order.objects.create(user = request.user,total_price = total_price, payment = order_payment,comments=user_comments,
                phone_number = phone_number_given, city = city, house_number = house_number, flat_number = flat_number, street = street, postal_code = postal_code, user_first_last_name = user_first_last_name)
                order.generateOrderId()
                order.generateSessionId()
                # order.sign = order.getRegistrationOrderSign()
                order.save()

                p24respon = json.loads(Przelewy24.registerPayment(order,request.user.email))
        

                for item in cart_products:
                    if item.product.is_promoted() == True:
                        obj = OrderItem.objects.create(product = item.product, order = order, product_name = item.product.name, quantity = item.quantity, price = item.product.promotion_price)
                    else:
                        obj = OrderItem.objects.create(product = item.product, order = order, product_name = item.product.name, quantity = item.quantity, price = item.product.price)
                cart_products.delete()
                messages.success(request,f'Zamówienie zostało złożone! Informacje na mailu!', extra_tags='order_completed')
                send_mail(f'Twoje zamówienie zostało zatwierdzone!',f'Zamówienie zostało złożone! Szacowany czas dostawy: 45 minut!',
                        EMAIL_HOST_USER, [email])
                send_mail(f'Nowe zamówienie od użytkownika {request.user.username}',f'Użytkownik {request.user.username} złożył zamówienie. Szczegóły w panelu.',
                        EMAIL_HOST_USER, [EMAIL_HOST_USER])

                try:
                    if "error" in p24respon:
                        print(p24respon)
                        messages.error(request, f'Błąd płatności')
                    elif "data" in p24respon:
                        result = p24respon["data"]
                        print(result)
                        print(p24respon["data"]["token"])
                        return redirect(P24['trnRequest']+str(p24respon["data"]["token"]))
                except:
                    messages.error(request, f'Błąd płatności')
            else:
                messages.error(request,f'Niepoprawne dane w formularzu')
        else:
            messages.error(request, f'Przed złożeniem zamówienia musisz dodać email.')
            return redirect('profile') 
    context = {'order_form': order_form, 'address_order_form': address_form,
    'final_realization_message': final_realization_message, 'final_realization_status': final_realization_status}
    return render(request,'menu/user_cart.html',context)


def add_to_cart(request,slug, quantity=1):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(slug=slug)
        order_item = Cart_item.objects.filter(cart = cart, product = product)
        if order_item.exists():
            item = Cart_item.objects.get(cart = cart, product = product)
            item.quantity += int(quantity)
            item.save()
            messages.success(request,'Produkt dodany do koszyka!', extra_tags='item_in_cart')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        else:
            cart_item = Cart_item(product = product, cart = cart, quantity = quantity)
            cart_item.save()
            messages.success(request,'Produkt dodany do koszyka!', extra_tags='item_added')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        response = redirect(('login'))
        response.set_cookie('product_before_login',slug)
        response.set_cookie('product_bef_login_quantity', quantity)
        return response


@login_required
def delete_from_cart(request,slug):
    cart = Cart.objects.get(user=request.user)
    product = Product.objects.get(slug=slug)
    cart_item = Cart_item.objects.get(cart = cart,product = product)
    if cart_item == None:
        pass
    else:
        cart_item.delete()
    messages.success(request,f'Produkt {product.name} usunięty z koszyka!', extra_tags='item_deleted')
    return redirect('user_cart')

@login_required
def product_quantity_increase(request,slug):
    cart = Cart.objects.get(user=request.user)
    product = Product.objects.get(slug=slug)
    cart_item = Cart_item.objects.get(cart = cart,product = product)
    cart_item.quantity += 1
    cart_item.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required
def product_quantity_decrease(request,slug):
    try:
        cart = Cart.objects.get(user=request.user)
        product = Product.objects.get(slug=slug)
        cart_item = Cart_item.objects.get(cart = cart,product = product)
        if cart_item.quantity == 1:
            cart_item.delete()
            #messages.success(request,f'Produkt {product.name} usunięty z koszyka!', extra_tags='item_deleted')
        else:
            cart_item.quantity -= 1
            cart_item.save()
    except Cart_item.DoesNotExist:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
