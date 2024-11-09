from django.db import models
from users.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator, ValidationError
from django.utils import timezone
from django.utils.text import slugify
from PIL import Image
from .payment import Przelewy24
import hashlib
from datetime import datetime
import random

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=20, blank=False, verbose_name='Nazwa kategori',unique=True)
    priority = models.DecimalField(default=1, verbose_name="Pozycja",blank = False, decimal_places = 3, max_digits=5)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Kategoria"
        verbose_name_plural = "Kategorie"

        default_permissions = []
        permissions = [
            ("add_category", "Użytkownik może dodawać"),
            ("change_category", "Użytkownik może zmieniać"),
            ("delete_category", "Użytkownik może usuwać"),
            ("view_category", "Użytkownik może wyświetlać"),
        ]

    
STATUS =  [
    (1, ("Dostępny")),
    (2, ("Niedostępny")),
]

class Ingredient(models.Model):
    name = models.CharField(max_length=40, blank=False, verbose_name="Nazwa")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Składnik"
        verbose_name_plural = "Składniki"

        default_permissions = []
        permissions = [
            ("add_ingredient", "Użytkownik może dodawać"),
            ("change_ingredient", "Użytkownik może zmieniać"),
            ("delete_ingredient", "Użytkownik może usuwać"),
            ("view_ingredient", "Użytkownik może wyświetlać"),
        ]

class Tag(models.Model):
    name = models.CharField(max_length=40, blank=False, verbose_name="Nazwa")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Etykieta"
        verbose_name_plural = "Etykiety"

        default_permissions = []
        permissions = [
            ("add_tag", "Użytkownik może dodawać"),
            ("change_tag", "Użytkownik może zmieniać"),
            ("delete_tag", "Użytkownik może usuwać"),
            ("view_tag", "Użytkownik może wyświetlać"),
        ]

class Allergen(models.Model):
    name = models.CharField(max_length=40, blank=False, verbose_name="Nazwa")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Allergen"
        verbose_name_plural = "Allergeny"

        default_permissions = []
        permissions = [
            ("add_allergen", "Użytkownik może dodawać"),
            ("change_allergen", "Użytkownik może zmieniać"),
            ("delete_allergen", "Użytkownik może usuwać"),
            ("view_allergen", "Użytkownik może wyświetlać"),
        ]

# def check_promoted_price(price):


class Product(models.Model):
    name = models.CharField(max_length=40, blank=False, verbose_name='Nazwa')
    description = models.TextField(blank=True, verbose_name='Opis')
    price = models.DecimalField(blank=False, default=0, verbose_name='Cena', decimal_places=2, max_digits=8)
    promotion_price = models.DecimalField(verbose_name="Kwota promocyjna",decimal_places=2, blank=True,null=True, max_digits= 8 )
    promotion_date_start = models.DateTimeField(verbose_name = 'Data początkowa promocji', blank=True,null=True)
    promotion_date_end = models.DateTimeField(verbose_name = 'Data końcowa promocji', blank=True, null=True)
    status = models.IntegerField(choices=STATUS, default=1, verbose_name='Status')
    kcal = models.IntegerField(default=0, verbose_name='Kcal', blank = True)
    categories = models.ManyToManyField(Category, verbose_name = "Kategorie")
    slug = models.SlugField(unique=True)
    image = models.ImageField(default = 'default_pic.png', upload_to='products_pics')
    ingredients = models.ManyToManyField(Ingredient, verbose_name='Składniki', blank = True)
    tags = models.ManyToManyField(Tag, verbose_name = 'Etykiety', blank = True)
    allergens = models.ManyToManyField(Allergen, verbose_name = 'Allergeny', blank = True)
   
    def __str__(self):
        return self.name

    def get_rating(self):
        sum = 0
        ratings = Rating.objects.filter(product=self)
        if len(ratings) == 0:
            return 0
        for rate in ratings:
            sum += rate.value
        return round(float(sum) / len(ratings),2)
    
    def ratings_count(self):
        ratings = Rating.objects.filter(product=self)
        return len(ratings)
    
    def get_comments(self):
        comments = Comment.objects.filter(product=self)
        return comments
    
    def comments_count(self):
        comments = Comment.objects.filter(product=self)
        return len(comments)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        if self.promotion_price is not None:
            if abs(self.promotion_price) >= self.price:
                raise ValidationError("Cena promocyjna nie może być większa niż cena wyjściowa!")
            # self.promotion_price = self.price    
        elif self.promotion_price is not None: 
            if self.promotion_price < 0:
                self.promotion_price = self.price + self.promotion_price
            # self.promotion_price = self.price
            elif self.promotion_price < 0:
                self.promotion_price = self.price + self.promotion_price
        super().save(*args, **kwargs)

        img = Image.open(self.image.path)
        value = 1000 #wartośc do scalowania
        if img.height > value or img.width > value:
            if img.height > img.width:
                proportion = float(img.height / value)
                height = float(img.height / proportion)
                width = float(img.width / proportion)
                resize_size = (width,height)
            else:
                proportion = float(img.width / value)
                height = float(img.height / proportion)
                width = float(img.width / proportion)
                resize_size = (width,height)
            img.thumbnail(resize_size)
            img.save(self.image.path)
        
    def is_promoted(self):
        if self.promotion_price == None or self.promotion_price == 0:
            return False
        else:
            if self.promotion_date_start == None or self.promotion_date_end == None:
                print("puste wartości w dacie")
                return False
            else:
                today = timezone.now()
                if today >= self.promotion_date_start and today <= self.promotion_date_end:
                    print("promocja obowiązuje")
                    return True
                else:
                    print("zły zakres daty")
                    return False

    class Meta:
        verbose_name = "Produkt"
        verbose_name_plural = "Produkty"

        default_permissions = []
        permissions = [
            ("add_product", "Użytkownik może dodawać"),
            ("change_product", "Użytkownik może zmieniać"),
            ("delete_product", "Użytkownik może usuwać"),
            ("view_product", "Użytkownik może wyświetlać"),
        ]

    

class Comment(models.Model):
    content = models.TextField(blank=False,verbose_name='')
    product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name = 'Produkt')
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, verbose_name = 'Użytkownik')
    created = models.DateTimeField(auto_now_add=True, verbose_name="Data utworzenia")
    
    def __str__(self):
        return f'{self.user} - {self.product}: {self.content}'

    class Meta:
        verbose_name = "Komentarz"
        verbose_name_plural = "Komentarze"

        default_permissions = []
        permissions = [
            ("add_comment", "Użytkownik może dodawać"),
            ("change_comment", "Użytkownik może zmieniać"),
            ("delete_comment", "Użytkownik może usuwać"),
            ("view_comment", "Użytkownik może wyświetlać"),
        ]

class Rating(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE, verbose_name = 'Produkt')
    user = models.ForeignKey(CustomUser, on_delete = models.CASCADE, verbose_name = 'Użytkownik')
    value = models.IntegerField(default=5, validators=[MinValueValidator(1), MaxValueValidator(5)],verbose_name="Wartość oceny")
    
    def __str__(self):
        return f'{self.user}: {self.value}'

    class Meta:
        unique_together = ('product','user') #by 1 ocena od usera
        verbose_name = "Ocena"
        verbose_name_plural = "Oceny"

        default_permissions = []
        permissions = [
            ("add_rating", "Użytkownik może dodawać"),
            ("change_rating", "Użytkownik może zmieniać"),
            ("delete_rating", "Użytkownik może usuwać"),
            ("view_rating", "Użytkownik może wyświetlać"),
        ]

PAYMENT =  [
    (1, ("Zapłać teraz"))
]

class Cart(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE, verbose_name = 'Użytkownik')
    status = models.IntegerField(choices=STATUS, default=1, verbose_name='Status zamówienia')
    cart_payment = models.IntegerField(choices=PAYMENT, default=1, verbose_name='Sposób płatności') #by przekazac wiadomosc przy tworzeniu orderu jest ten stworzony argument
    
    class Meta:
        verbose_name = "Koszyk"
        verbose_name_plural = "Koszyki"

        default_permissions = []
        permissions = [
            ("add_cart", "Użytkownik może dodawać"),
            ("change_cart", "Użytkownik może zmieniać"),
            ("delete_cart", "Użytkownik może usuwać"),
            ("view_cart", "Użytkownik może wyświetlać"),
        ]

    def __str__(self):
        return f'Koszyk użytkownika: {self.user}'


    def get_total_price(self):
        sum = 0
        for item in Cart_item.objects.filter(cart=self):
            if item.product.is_promoted() == True:
                sum += item.product.promotion_price * item.quantity
            else:
                sum += item.product.price * item.quantity
        return float(sum)
    
    def get_amount(self):
        return len(Order_item.objects.filter(cart=self))

    
    # def save(self,*args, **kwargs):
    #     if self.status == 2:
    #         total_price = 0 #cena koszyka
    #         cart_products = Cart_item.objects.filter(cart=self) #wszystkie produkty w koszyku
    #         for item in cart_products:
    #             total_price += item.product.price * item.quantity
    #         order = Order.objects.create(user = self.user,total_price = total_price, payment = self.cart_payment)
    #         for item in cart_products:
    #             obj = OrderItem.objects.create(product = item.product, order = order, product_name = item.product.name, quantity = item.quantity, price = item.product.price)
    #         self.status = 1
    #         cart_products.delete()
            
    #     super(Cart, self).save(*args,**kwargs)

    

class Cart_item(models.Model):
    product = models.ForeignKey(Product, verbose_name="Produkt", on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, verbose_name="Zamówienie", on_delete=models.CASCADE, related_name="cart_items")
    date_added = models.DateTimeField(auto_now_add=True)
    quantity = models.IntegerField(default = 1)
    
    def __str__(self):
        return f'{self.product} - produkt w zamówieniu  {self.cart.user}'

    class Meta:
        unique_together = ['product','cart']
        verbose_name = "Przedmiot w koszyku"
        verbose_name_plural = "Przedmioty w koszyku"

        default_permissions = []
        permissions = [
            ("add_cart_item", "Użytkownik może dodawać"),
            ("change_cart_item", "Użytkownik może zmieniać"),
            ("delete_cart_item", "Użytkownik może usuwać"),
            ("view_cart_item", "Użytkownik może wyświetlać"),
        ]

    @property #zwraca wartosc ostateczna za dany produkt w koszyku
    def priceXquantity(self):
        if self.product.is_promoted() == True:
            print("promocja dobrze mnoznona")
            return float(self.quantity * self.product.promotion_price)
        print("promocja nie jest dobrze mnoznona")
        return float(self.quantity * self.product.price)

STATUS =  [
    (1, ("Nowe")),
    (2, ("Opłacone")),
    (3, ("W trakcie realizacji")),
    (4, ("Zrealizowane")),
    (5, ("Anulowane")),
]

PAYMENT_STATUS =  [
    (0, ("Nieopłacone")),
    (1, ("Nieopłacone")),
    (2, ("Opłacone")),
]

class Order(models.Model):
    user = models.ForeignKey(CustomUser,on_delete=models.SET_NULL, null = True, verbose_name = "Użytkownik")
    status = models.IntegerField(choices=STATUS, default=1, verbose_name='Status zamówienia')
    total_price = models.FloatField(default=0, verbose_name="Kwota zamówienia")
    created = models.DateTimeField(auto_now_add=True, verbose_name="Data zamówienia")
    payment = models.IntegerField(choices=PAYMENT, default=1, verbose_name='Sposób płatności')
    payment_status = models.IntegerField(choices = PAYMENT_STATUS,default=0, verbose_name="Status płatności")
    user_first_last_name = models.CharField(verbose_name="Imię i Nazwisko", max_length=60, blank=True)
    comments = models.TextField(verbose_name="Uwagi", blank=True)
    phone_number = models.CharField(verbose_name= "Numer telefonu",max_length=30, unique= False, blank=True)
    city = models.CharField(verbose_name= "Miejscowość",max_length=30, blank=True)
    house_number = models.CharField(verbose_name= "Numer domu",max_length=5, blank=True)
    flat_number = models.CharField(verbose_name= "Numer mieszkania",max_length=5, blank=True)
    street = models.CharField(verbose_name= "Ulica",max_length=40, blank=True)
    postal_code = models.CharField(verbose_name= "Kod pocztowy",max_length=15, blank=True)
    sessionId = models.CharField(verbose_name='Id zamówienia P24', blank = True, max_length=100, default='1')
    orderId = models.CharField(verbose_name="Id zamówienia", blank=False, unique = True, max_length=100)
    paymentOrderId = models.CharField(verbose_name="Id zamówienia nadany przez P24", blank=True, unique = False, max_length=100, default = '0')
    currency = models.CharField(verbose_name='Waluta', default="PLN", max_length=3) 
    sign = models.CharField(verbose_name='Unikatowy znak', blank = True, max_length=100)
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     if len(self.orderId) == 0 or self.orderId == '0':
    #         self.generateOrderId()

    def getRegistrationOrderSign(self):
        crcKey = Przelewy24.crcKey
        merchantId = Przelewy24.id
        toMd5 = "{\"sessionId\":\""+self.sessionId+"\","
        toMd5 += "\"merchantId\":"+str(merchantId)+","
        toMd5 += "\"amount\":"+str(int(self.total_price * 100))+","
        toMd5 += "\"currency\":\""+self.currency + "\","
        toMd5 += "\"crc\":\""+crcKey + "\"}"
        # print(toMd5)
        self.sign = hashlib.sha384(toMd5.encode()).hexdigest()
        #print(self.sign)
        return self.sign

    def getVerifySign(self):
        crcKey = Przelewy24.crcKey
        merchantId = Przelewy24.id
        toMd5 = "{\"sessionId\":\""+self.sessionId+"\","
        toMd5 += "\"orderId\":"+str(self.paymentOrderId)+","
        toMd5 += "\"amount\":"+str(self.total_price * 100)[:-2]+","
        toMd5 += "\"currency\":\""+self.currency + "\","
        toMd5 += "\"crc\":\""+crcKey + "\"}"
        #print(toMd5)
        self.sign = hashlib.sha384(toMd5.encode()).hexdigest()
        #print(self.sign)
        return self.sign

    def generateSessionId(self):
        if len(self.sessionId)>0 and self.sessionId != '1':
            inc = int(self.sessionId[-1])+1
            self.sessionId = self.sessionId[:-1]+str(inc)
        else:
            self.sessionId = self.orderId+"1"

    def generateOrderId(self):
        self.orderId = str(self.id)+datetime.now().strftime("%y%m%d")+str(random.randint(1,9))

    def copySessionToOrder(self):
        self.orderId = self.sessionId

    def get_total_price(self):
        return self.total_price

    def get_delivery_price(self):
        return self.total_price-self.get_products_total_price()

    def get_products_total_price(self):
        products = OrderItem.objects.filter(order=self)
        total_price = 0
        for product in products:
            total_price += product.price*product.quantity
        return total_price

    def get_ordered_products(self):
        return list(enumerate(OrderItem.objects.filter(order=self)))

    def get_ordered_productsStrTruncate(self):
        productsStr = ""
        products = list(enumerate(OrderItem.objects.filter(order=self)))
        charscount = 0
        for index, product in products:
            if charscount > 30:
                productsStr += "..."
                break
            else:
                productsStr += product.product_name
                charscount += len(productsStr)
                if len(products) > 1 and index<len(products)-1:
                    productsStr += ", "
        return productsStr

    def statusStr(self):
        return dict(STATUS)[self.status]

    def __str__(self):
        return f'Zamówiony produkt użytkownika {self.user}'

    class Meta:
        verbose_name = "Zamówienie"
        verbose_name_plural = "Zamówienia"

        default_permissions = []
        permissions = [
            ("add_order", "Użytkownik może dodawać"),
            ("change_order", "Użytkownik może zmieniać"),
            ("delete_order", "Użytkownik może usuwać"),
            ("view_order", "Użytkownik może wyświetlać"),
        ]
    

class OrderItem(models.Model):
    product = models.ForeignKey(Product,verbose_name="Produkt", on_delete = models.SET_NULL, null = True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE,related_name='order_items')
    created = models.DateTimeField(auto_now_add=True,verbose_name='Data zamówienia')
    product_name = models.CharField(max_length=40, verbose_name='Nazwa produktu')
    quantity = models.IntegerField(default = 1, verbose_name='Ilość')
    price = models.FloatField(blank=False, default=0, verbose_name='Cena')

    class Meta:
        verbose_name = "Zamówiony produkt"
        verbose_name_plural = "Zamówione produkty"

        default_permissions = []
        permissions = [
            ("add_orderitem", "Użytkownik może dodawać"),
            ("change_orderitem", "Użytkownik może zmieniać"),
            ("delete_orderitem", "Użytkownik może usuwać"),
            ("view_orderitem", "Użytkownik może wyświetlać"),
        ]

    def totalPrice(self):
        return self.price*self.quantity

    def __str__(self):
        return f'Zfinalizowany product {self.product_name} użytkownika {self.order.user}' 
    








