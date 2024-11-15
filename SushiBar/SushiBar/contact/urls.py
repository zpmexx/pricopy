from importlib import import_module

from django.urls import include, path, re_path

from allauth.socialaccount import providers

from . import app_settings

from allauth.account import views

from .views import allauthloginview

urlpatterns = [
    path("logout/", views.logout, name="account_logout"),
    # path(
    #     "password/change/",
    #     views.password_change,
    #     name="account_change_password",
    # ),
    # path("password/set/", views.password_set, name="account_set_password"),
    # path("inactive/", views.account_inactive, name="account_inactive"),
    # E-mail
    # path("email/", views.email, name="account_email"),
    path(
        "confirm-email/",
        views.email_verification_sent,
        name="account_email_verification_sent",
    ),
        path(
        "login/cancelled/",
        views.email_verification_sent,
        name="account_email_verification_sent",
    ),
    re_path(
        r"^confirm-email/(?P<key>[-:\w]+)/$",
        views.confirm_email,
        name="account_confirm_email",
    ),
    # password reset
    # path("password/reset/", views.password_reset, name="account_reset_password"),
    # path(
    #     "password/reset/done/",
    #     views.password_reset_done,
    #     name="account_reset_password_done",
    # ),
    # re_path(
    #     r"^password/reset/key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$",
    #     views.password_reset_from_key,
    #     name="account_reset_password_from_key",
    # ),
    # path(
    #     "password/reset/key/done/",
    #     views.password_reset_from_key_done,
    #     name="account_reset_password_from_key_done",
    # ),
]

if app_settings.SOCIALACCOUNT_ENABLED:
    urlpatterns += [path("social/", include("allauth.socialaccount.urls"))]

# Provider urlpatterns, as separate attribute (for reusability).
provider_urlpatterns = []
for provider in providers.registry.get_list():
    try:
        prov_mod = import_module(provider.get_package() + ".urls")
    except ImportError:
        continue
    prov_urlpatterns = getattr(prov_mod, "urlpatterns", None)
    if prov_urlpatterns:
        provider_urlpatterns += prov_urlpatterns
urlpatterns += provider_urlpatterns