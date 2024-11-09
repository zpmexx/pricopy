from django.contrib.auth import views as auth_views

class PasswordResetViewOwn(auth_views.PasswordResetView):
    email_template_name = 'users/email.html'