from django.db import models
from django.core.exceptions import ValidationError
from datetime import datetime 
from django.utils import timezone
from django.core.validators import MinValueValidator
# # Create your models here.
#informacje o restauracji
class BarInformations(models.Model):
    street = models.CharField(max_length=40, blank=False, default='ul. Głogowska 158', verbose_name='Ulica')
    city = models.CharField(max_length=20, blank=False, default='Poznań', verbose_name='Miasto')
    code = models.CharField(max_length=20, blank=False, default='60-132',verbose_name='Kod pocztowy')
    number = models.PositiveIntegerField(blank=False, default=699898244, verbose_name = 'Numer telefonu')
    email = models.EmailField(max_length=40, default='kontakt@yakitori-grill.pl', verbose_name='Adres Email')
    delivery_cost = models.DecimalField(default = 8,decimal_places=2, max_digits=4, validators=[MinValueValidator(0)], verbose_name='Koszt dostawy')

    def __str__(self):
        return f'{self.city}, {self.street}, {self.email}'
    
    class Meta:
        verbose_name = "Informacje o restauracji"
        verbose_name_plural = "Informacje o restauracji"   

        default_permissions = []
        permissions = [
            ("add_barinformations", "Użytkownik może dodawać"),
            ("change_barinformations", "Użytkownik może zmieniać"),
            ("delete_barinformations", "Użytkownik może usuwać"),
            ("view_barinformations", "Użytkownik może wyświetlać"),
        ]
    def save(self, *args, **kwargs):
        if not self.pk and BarInformations.objects.exists():
            raise ValidationError('Może występować tylko jeden adres!')
        return super(BarInformations, self).save(*args, **kwargs)

WEEKDAYS = [
  (0, ("Poniedziałek")),
  (1, ("Wtorek")),
  (2, ("Środa")),
  (3, ("Czwartek")),
  (4, ("Piatek")),
  (5, ("Sobota")),
  (6, ("Niedziela")),
]
#godziny otwarcia
class OpeningHours(models.Model):
    weekday = models.IntegerField(choices=WEEKDAYS, verbose_name='Dzień tygodnia')
    from_hour = models.TimeField(verbose_name='Otwarte od godziny')
    to_hour = models.TimeField(verbose_name='Zamkniecie o godzinie')

    class Meta:
        ordering = ('weekday', 'from_hour') #sortowanie 
        unique_together = ('weekday', 'from_hour', 'to_hour') #unikalna wartosc gdy 3 wspolnie będą takie same
        verbose_name = "Godziny otwarcia"
        verbose_name_plural = "Godziny otwarcia"

        default_permissions = []
        permissions = [
            ("add_openinghours", "Użytkownik może dodawać"),
            ("change_openinghours", "Użytkownik może zmieniać"),
            ("delete_openinghours", "Użytkownik może usuwać"),
            ("view_openinghours", "Użytkownik może wyświetlać"),
        ]
    
    
    def __str__(self):
        return f'{self.get_weekday_display()}: {self.from_hour} - {self.to_hour}' #reprezentacja obiektu

    def get_weekday(self):
        return self.get_weekday_display()

    def get_from_hour_hour(self):
        return self.from_hour.hour
    
    def get_from_hour_minute(self):
        return self.from_hour.minute
    
    def get_to_hour_hour(self):
        return self.to_hour.hour
    
    def get_to_hour_minute(self):
        return self.to_hour.minute

STATUS = [
  (1, ("Do realizacji")),
  (2, ("Zatwierdzone")),
]

class ContactModel(models.Model):
    name = models.CharField(max_length=15, blank=False, verbose_name="Użytkownik")
    email = models.EmailField(max_length=40, blank=False, verbose_name="Email")
    title = models.CharField(max_length=40, blank=False, verbose_name="Tytuł zgłoszenia")
    content = models.TextField(blank=False, verbose_name="Treść")
    # date = models.DateTimeField(default=datetime.now())
    date = models.DateTimeField(default = timezone.now)
    status = models.IntegerField(choices=STATUS, default=1)

    class Meta:
        ordering = ('status', '-date') #sortowanie 
        verbose_name = "Zgłoszenie"
        verbose_name_plural = "Zgłoszenia"

        default_permissions = []
        permissions = [
            ("add_contactmodel", "Użytkownik może dodawać"),
            ("change_contactmodel", "Użytkownik może zmieniać"),
            ("delete_contactmodel", "Użytkownik może usuwać"),
            ("view_contactmodel", "Użytkownik może wyświetlać"),
        ]
    
    
    def __str__(self):
        return f'{self.get_status_display()}: {self.name} - {self.title}'
RESTAURAT_STATUS = [
  (1, ("Otwarta")),
  (2, ("Zamknięta")),
]


class RealizationHours(models.Model):
    weekday = models.IntegerField(choices=WEEKDAYS, verbose_name='Dzień tygodnia', unique = True)
    from_hour = models.TimeField(verbose_name='Godzina początkowa', default = '8:00:00')
    to_hour = models.TimeField(verbose_name='Godzina końcowa', default = '21:00:00')
    status = models.IntegerField(choices=RESTAURAT_STATUS, verbose_name='Status otwarcia restauracji', default = 1)

    def __str__(self):
        return self.get_weekday_display()
    class Meta:

        ordering = ('weekday', 'from_hour') #sortowanie 
        verbose_name = ('Dzień tygodnia')
        verbose_name_plural = "Godziny przyjmowania zamówień"

        default_permissions = []
        permissions = [
            ("add_realizationhours", "Użytkownik może dodawać"),
            ("change_realizationhours", "Użytkownik może zmieniać"),
            ("delete_realizationhours", "Użytkownik może usuwać"),
            ("view_realizationhours", "Użytkownik może wyświetlać"),
        ]
    def get_weekday(self):
        return self.get_weekday_display()

    def get_from_hour_hour(self):
        return self.from_hour.hour
    
    def get_from_hour_minute(self):
        return self.from_hour.minute
    
    def get_to_hour_hour(self):
        return self.to_hour.hour
    
    def get_to_hour_minute(self):
        return self.to_hour.minute

STATUSREALIZATION = [
  (1, ("Otwarta")),
  (2, ("Zamknięta na czas określony")),
  (3, ("Zamknięta do odwołania")),
]

class RealizationStatus(models.Model):
    status = models.IntegerField(choices=STATUSREALIZATION, verbose_name='Możliwośc realizacji zamówień', default=1)
    from_date = models.DateTimeField(verbose_name='Data początkowa')
    to_date = models.DateTimeField(verbose_name='Data końcowa')
    message = models.TextField(blank=True, verbose_name='Informacja dla klienta')

    def __str__(self):
        return f'Obecny możliwość zamówień: {self.get_status_display()}'

    class Meta:
        verbose_name = ('Status możliwości dokonywania zamówień przez klientów')
        verbose_name_plural = "Status możliwości dokonywania zamówień przez klientów"

        default_permissions = []
        permissions = [
            ("add_realizationstatus", "Użytkownik może dodawać"),
            ("change_realizationstatus", "Użytkownik może zmieniać"),
            ("delete_realizationstatus", "Użytkownik może usuwać"),
            ("view_realizationstatus", "Użytkownik może wyświetlać"),
        ]
    def save(self, *args, **kwargs):
        if not self.pk and RealizationStatus.objects.exists():
            raise ValidationError('Może występować tylko jeden status!')
        return super(RealizationStatus, self).save(*args, **kwargs)

    # brak możliwości nadpisana obiektu - można potem pomysleć by w editorze wyłączyć taką możliwość zamiast na modelu 
    # def save(self, *args, **kwargs):
    #     if self.pk:
    #         raise ValidationError(f'Nie możesz zmienic tresci formularza kontaktowego {self.title}')
    #     super(ContactModel, self).save(*args, **kwargs)

    