from django.db import models
from datetime import datetime 
from PIL import Image
from django.utils import timezone
# Create your models here.
# obiekt aktualności 
class News(models.Model):
    title = models.CharField(max_length=30, blank=False, verbose_name='Tytuł')
    short_content = models.CharField(max_length=60, blank=False, default='Domyślny opis', verbose_name="Opis")
    content = models.TextField(blank=False, default='Domyślna treść',verbose_name='Treść')
    image = models.ImageField(default = 'default_pic.jpg', upload_to='news_pics',verbose_name='Zdjęcie')
    # date = models.DateTimeField(default=datetime.now())
    date = models.DateTimeField(default = timezone.now)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.title

    # nadpisanie metody save zapisującej zdjecie do folderu 'static' po zmniejszeniu go do oczekiwanego rozmiaru 
    def save(self, *args, **kwargs):
        super(News, self).save(*args, **kwargs)

        img = Image.open(self.image.path)

        if img.height > 300 or img.width > 300:
            resize_size = (300,300) #rozmiar zdjecia do którego zostaje ono pomniejszone
            img.thumbnail(resize_size)
            img.save(self.image.path)
    class Meta:
        verbose_name = "Aktualność"
        verbose_name_plural = "Aktualności"
        unique_together = ('title','slug')

        default_permissions = []
        permissions = [
            ("add_news", "Użytkownik może dodawać"),
            ("change_news", "Użytkownik może zmieniać"),
            ("delete_news", "Użytkownik może usuwać"),
            ("view_news", "Użytkownik może wyświetlać"),
        ]

class MainSiteText(models.Model):
    content = models.TextField(blank = False, default="Domyślna treść na stronie głównej", verbose_name='Tekst') #można będzie później nadpisać save, by tylko jedne obiekt mógł być
    
    def __str__(self):
        return f'Tekst na stronie głównej'
    class Meta:
        verbose_name = "Teskt na stronie głównej"
        verbose_name_plural = "Tekst na stronie głównej"

        default_permissions = []
        permissions = [
            ("add_mainsitetext", "Użytkownik może dodawać"),
            ("change_mainsitetext", "Użytkownik może zmieniać"),
            ("delete_mainsitetext", "Użytkownik może usuwać"),
            ("view_mainsitetext", "Użytkownik może wyświetlać"),
        ]
