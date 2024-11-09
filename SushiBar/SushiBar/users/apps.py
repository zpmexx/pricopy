from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'users'
    verbose_name = 'Użytkownicy'

    def ready(self):
        import users.signals


        