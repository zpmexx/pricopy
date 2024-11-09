from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.


class AboutUs(models.Model):
    title = models.CharField(verbose_name='Tytuł', max_length=50, unique=True)
    content = RichTextUploadingField(verbose_name="Treść", config_name='aboutus_ckeditor')
    date_created = models.DateTimeField(verbose_name='Data modyfikacji', auto_now=True)


    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = "O nas"
        verbose_name_plural = "O nas"

        default_permissions = []
        permissions = [
            ("add_aboutus", "Użytkownik może dodawać"),
            ("change_aboutus", "Użytkownik może zmieniać"),
            ("delete_aboutus", "Użytkownik może usuwać"),
            ("view_aboutus", "Użytkownik może wyświetlać"),
        ]
    
        
    