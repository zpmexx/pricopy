from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter
from allauth.exceptions import ImmediateHttpResponse
from allauth.socialaccount.signals import pre_social_login
from allauth.account.utils import perform_login
from allauth.utils import get_user_model
from django.http import HttpResponse
from django.dispatch import receiver
from django.shortcuts import redirect
from django.conf import settings
import json
from django.core.exceptions import ValidationError
from django.shortcuts import resolve_url
from django.contrib.auth import logout

def logout_view(request):
    logout(request)


class MyLoginAccountAdapter(DefaultAccountAdapter):
    '''
    Overrides allauth.account.adapter.DefaultAccountAdapter.ajax_response to avoid changing
    the HTTP status_code to 400
    '''

    def get_login_redirect_url(self, request):
        """ 
        """
        if request.user.is_authenticated:
            if request.user.username == 'user':
                User = get_user_model()
                users = User.objects.all().count()
                request.user.username = 'Użytkownik' + str(users+1)
                request.user.save()
            url = settings.LOGIN_URL
            return resolve_url(url)
        else:
            return "/"


class MySocialAccountAdapter(DefaultSocialAccountAdapter):
    '''
    Overrides allauth.socialaccount.adapter.DefaultSocialAccountAdapter.pre_social_login to 
    perform some actions right after successful login
    '''
    def pre_social_login(self, request, sociallogin):


        print(request.user)


            # TODOFuture: To perform some actions right after successful login

@receiver(pre_social_login)
def link_to_local_user(sender, request, sociallogin, **kwargs):
    ''' Login and redirect
    This is done in order to tackle the situation where user's email retrieved
    from one provider is different from already existing email in the database
    (e.g facebook and google both use same email-id). Specifically, this is done to
    tackle following issues:
    * https://github.com/pennersr/django-allauth/issues/215

    '''
    try:
        email_address = sociallogin.account.extra_data['email']
    except:
        response = redirect('logout')
        return response
    User = get_user_model()
    users = User.objects.filter(email=email_address)
    if users:
        response = redirect(settings.LOGIN_REDIRECT_URL.format(id=request.user.id))
        # allauth.account.app_settings.EmailVerificationMethod
        perform_login(request, users[0], email_verification='optional')
        raise ImmediateHttpResponse(response)

            # if user is not None:
            #     if request.COOKIES.get('product_before_login') is None:
            #         login(request, user)
            #         return redirect('main')
            #     else:
            #         response = redirect(('main'))
            #         cart = Cart.objects.get(user=user)
            #         product = Product.objects.get(slug=request.COOKIES.get('product_before_login'))
            #         order_item = Cart_item.objects.filter(cart = cart, product = product)
            #         if order_item.exists():
            #             item = Cart_item.objects.get(cart = cart, product = product)
            #             item.quantity += 1
            #             item.save()
            #         else:
            #             cart_item = Cart_item(product = product, cart = cart, quantity = 1)
            #             cart_item.save()
            #         login(request, user)
            #         response.delete_cookie('product_before_login')
            #         return response

