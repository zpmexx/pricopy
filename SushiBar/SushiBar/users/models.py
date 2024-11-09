from django.db import models
from PIL import Image
from django.utils.http import urlquote
# from django.utils.translation import ugettext_lazy as _
from django.core.mail import send_mail
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils.text import slugify


class CustomUserManager(BaseUserManager):

    def _create_user(self, username, email, phone_number, password,
                     is_staff, is_superuser, **extra_fields):

        if not email:
            raise ValueError('Brak maila')
        if not username:
            raise ValueError('Brak nazwy użytkownika')
        email = self.normalize_email(email)
        user = self.model(username = username, email=email, phone_number=phone_number,
                          is_staff=is_staff, is_active=True,
                          is_superuser=is_superuser,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email, phone_number, password=None, **extra_fields):
        return self._create_user(username, email, phone_number, password, False, False,
                                 **extra_fields)

    def create_superuser(self, username, email, phone_number, password, **extra_fields):
        return self._create_user(username, email, phone_number, password, True, True,
                                 **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='Email', max_length=50, unique=True, error_messages={'required': ''})
    username = models.CharField(verbose_name= "Nazwa użytkownika",max_length=30, unique=True)
    phone_number = models.CharField(verbose_name= "Numer telefonu",max_length=30, unique= False) #unique = True na wdrożeniu
    is_staff = models.BooleanField(verbose_name='Osługa', default=False,
        help_text='Decyduje czy użytkownik może zalogować się do panelu admina')
    is_active = models.BooleanField(verbose_name='Aktywność konta', default=True,
        help_text='Decyduje czy konto jest włączone. Zalecane jest wyłączanie zamiast usuwania konta')
    date_joined = models.DateTimeField(verbose_name='Data dołączenia', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='Data ostatniego logowania', auto_now=True)
    is_superuser = models.BooleanField(verbose_name='Konto admina', default=False,
        help_text='Konto umożliwiające zrobienie absolutnie wszystkiego w panelu admina, "superuser".')
    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email','phone_number']

    class Meta:
        verbose_name = ('Użytkownik')
        verbose_name_plural = ('Użytkownicy')

        default_permissions = []
        permissions = [
            ("add_customuser", "Użytkownik może dodawać"),
            ("change_customuser", "Użytkownik może zmieniać"),
            ("delete_customuser", "Użytkownik może usuwać"),
            ("view_customuser", "Użytkownik może wyświetlać"),
        ]


    # def get_absolute_url(self):
    #     return "/users/%s/" % urlquote(self.email) ## tu mozna zalinkowac profil

    def get_full_name(self):
        full_name = f'{self.email}'
        return full_name

    def get_short_name(self):
        return self.email

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

    def __str__(self):
        return self.username
    
    

class Profile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    image = models.ImageField(default = 'avatar_default.jpg', upload_to = 'profile_pics', verbose_name="Zdjęcie")
    
    def __str__(self):
        return f'Profil użytkownika {self.user.username}'
    
    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            resize_size = (300,300)
            img.thumbnail(resize_size)
            img.save(self.image.path)
    
    class Meta:
        verbose_name = "Profil"
        verbose_name_plural = "Profile Użytkowników"

        default_permissions = []
        permissions = [
            ("add_profile", "Użytkownik może dodawać"),
            ("change_profile", "Użytkownik może zmieniać"),
            ("delete_profile", "Użytkownik może usuwać"),
            ("view_profile", "Użytkownik może wyświetlać"),
        ]

class Address(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    user_first_last_name = models.CharField(verbose_name="Imię i Nazwisko", max_length=60)
    city = models.CharField(verbose_name= "Miejscowość",max_length=30)
    house_number = models.CharField(verbose_name= "Numer domu",max_length=5)
    flat_number = models.CharField(verbose_name= "Numer mieszkania",max_length=5, blank= True)
    street = models.CharField(verbose_name= "Ulica",max_length=40)
    postal_code = models.CharField(verbose_name= "Kod pocztowy",max_length=15)


    
    def __str__(self):
        return f'Adres użytkownika {self.user.username}'
    
    class Meta:
        verbose_name = "Adres"
        verbose_name_plural = "Adresy"

        default_permissions = []
        permissions = [
            ("add_address", "Użytkownik może dodawać"),
            ("change_address", "Użytkownik może zmieniać"),
            ("delete_address", "Użytkownik może usuwać"),
            ("view_address", "Użytkownik może wyświetlać"),
        ]

class VisitStatistics(models.Model):
    date = models.DateField(auto_now=True ,verbose_name='Data wizyty')
    time = models.TimeField(auto_now_add=True, verbose_name = 'Godzina wizyty')
    visited_site = models.CharField(verbose_name= "Strona",max_length=100)
    ip = models.CharField(verbose_name= "Adres IP",max_length=100)
    system = models.CharField(verbose_name= "System",max_length=100)
    browser = models.CharField(verbose_name= "Przeglądarka",max_length=100)

    def __str__(self):
        return f'Wizyta z adresu {self.ip}'

    class Meta:
        verbose_name = "Odwiedziny"
        verbose_name_plural = "Lista odwiedzin"

        default_permissions = []
        permissions = [
            ("add_visitstatistics", "Użytkownik może dodawać"),
            ("change_visitstatistics", "Użytkownik może zmieniać"),
            ("delete_visitstatistics", "Użytkownik może usuwać"),
            ("view_visitstatistics", "Użytkownik może wyświetlać"),
        ]