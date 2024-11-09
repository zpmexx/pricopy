"""SushiBar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include, re_path
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views
from django.contrib.auth import views as auth_views
from contact import views as contact_views
from about import views as about_views
from menu import views as menu_views
from django.conf.urls.i18n import i18n_patterns
from django.views.generic.base import RedirectView, TemplateView
from users.reset import PasswordResetViewOwn
from news.views import news_list, news_detail
from django.contrib.staticfiles.storage import staticfiles_storage



urlpatterns = [
    path('yakiadmin/', admin.site.urls, name = 'admin'),
    path('', RedirectView.as_view(url='/menu', permanent=False), name = 'main'),
    path('menu/', include('menu.urls')),
	path('news/', include('news.urls')),
    path('logowanie/', user_views.loginPage, name='login'),
    path('rejestracja/', user_views.registerPage, name='register'),
    path('wylogowanie/', user_views.logoutPage, name='logout'),
    path('profil/', user_views.profile, name='profile'),
    path('zamowienia/', user_views.ordersPage, name='zamowienia'),
    path('zamowienia/<orderId>', user_views.orderPage, name='zamowienie'),
    path('koszyk/', menu_views.user_cart_view, name='user_cart'),
    path('reset_hasła/',PasswordResetViewOwn.as_view(template_name="users/reset.html"), name="password_reset"),
    path('reset_hasło_wysłane/', auth_views.PasswordResetDoneView.as_view(template_name="users/reset_sent.html"), name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='users/reset_confirm.html'), name='password_reset_confirm'),
    path('reset_sukces/', auth_views.PasswordResetCompleteView.as_view(template_name="users/reset_success.html"), name="password_reset_complete"),
    path('kontakt/', contact_views.contactFormView, name='contact'),
    path('o_nas/',about_views.about_us_view, name = 'about'),
    path('accounts/social/login/cancelled/', contact_views.allauthloginview, name='allauthlogin'),
    path('accounts/', include('contact.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    #API
    path('api/', include('users.restapi.urls')),
    path('api/users/', include('users.restapi.urls')),
    path('api/news/', include('news.restapi.urls', 'news_api')),
    path('api/menu/', include('menu.restapi.urls', 'menu_api')),
    #END API
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('i18n/', include('django.conf.urls.i18n')),  # Make sure this is present
    path('favicon.ico', RedirectView.as_view(url=staticfiles_storage.url('favicon.ico'))),
    re_path(r'^kuchnia/(?:.*)/?$', TemplateView.as_view(template_name='react_webpack.html'))

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# handler400 = about_views.bad_request_400
# handler403 = about_views.permission_denied_403
# handler404 = about_views.page_not_found_404
# handler500 = about_views.server_error_500
