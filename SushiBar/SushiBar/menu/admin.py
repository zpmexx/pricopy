from django.contrib import admin
from .models import Product, Category, Comment, Cart, Cart_item, Order, OrderItem, Rating, Ingredient, Tag, Allergen
# Register your models here.

class CategoryAdmin(admin.ModelAdmin):
    model = Category
    list_display = ['priority','name',]
    search_fields = ['name']
    ordering = ['priority','name']

admin.site.register(Category,CategoryAdmin)

class IngredientAdmin(admin.ModelAdmin):
    model = Ingredient
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Ingredient,IngredientAdmin)

class TagAdmin(admin.ModelAdmin):
    model = Tag
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Tag,TagAdmin)

class AllergenAdmin(admin.ModelAdmin):
    model = Allergen
    list_display = ['name']
    search_fields = ['name']

admin.site.register(Allergen,AllergenAdmin)

class ProductAdmin(admin.ModelAdmin):
    model = Product
    list_display = ['name','price','promoted_price','promoted','status','get_categories']
    list_filter = ['status']
    search_fields = ['name','status','categories__name']
    ordering = ['status','name']
    fieldsets = (
        ('Informacje o produkcie', { 'fields': ('name','slug','description','status','kcal')}),
        ('Informacje o cenie', {'fields': ('price','promotion_price','promotion_date_start','promotion_date_end')}),
        ('Pozostałe informacje', {'fields': ('categories','ingredients','tags','allergens','image')})
    )
    prepopulated_fields = {"slug": ("name",)}

    def get_categories(self,obj):
        return "\n,".join([p.name for p in obj.categories.all()])
    get_categories.short_description = 'Kategorie'

    def promoted_price(self,obj):
        if obj.is_promoted():
            return obj.promotion_price
        return '-'
    promoted_price.short_description = 'Cena promocyjna'

    def promoted(self,obj):
        if obj.is_promoted():
            return 'Aktywna'
        return 'Nieaktywna'
    promoted.short_description = 'Status promocji'


    
admin.site.register(Product,ProductAdmin)

class CommentAdmin(admin.ModelAdmin):
    model = Comment
    list_display = ['user','product','created']
    ordering = ['created','product','user']
    search_fields = ['user__username','product__name']

admin.site.register(Comment,CommentAdmin)

class RatingAdmin(admin.ModelAdmin):
    model = Rating
    list_display = ['user','product','value']
    ordering = ['product','user','value']
    search_fields = ['user__username','product__name']

admin.site.register(Rating,RatingAdmin)

class CartAdmin(admin.ModelAdmin):
    model = Cart
    list_display = ['user']
    ordering = ['user']
    search_fields = ['user']
    exclude = ('status','cart_payment')

admin.site.register(Cart,CartAdmin)

class CartItemAdmin(admin.ModelAdmin):
    model = Cart_item
    list_display = ['product','cart_user','date_added']
    ordering = ['date_added','product']
    search_fields = ['product']

    def cart_user(self,obj):
        return obj.cart.user
    cart_user.short_description = "Użytkownik"
    cart_user.admin_order_field = 'cart.user'

admin.site.register(Cart_item,CartItemAdmin)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    fields = ['product','quantity','price']
    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
    readonly_fields = ['product','quantity','price']

class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['orderId', 'sessionId', 'created','status','user','total_price']
    ordering = ['status','created']
    fieldsets = (
        ('Informacje o użytkowniku', { 'fields': ('user_first_last_name','user','phone_number','city','postal_code','street',('house_number','flat_number'))}),
        ('Informacje o zamówieniu', {'fields': ('orderId', 'sessionId', 'status','payment','payment_status','total_price','comments',)})
    )
    inlines = [
        OrderItemInline,
    ]
    # readonly_fields = ['user_first_last_name','user','phone_number','city','postal_code','street','house_number','flat_number','payment','payment_status','total_price','comments']
    readonly_fields = ['orderId', 'sessionId', 'user','payment','payment_status']
    search_fields = ['sessionId','user__username','status']
    # list_per_page = 10 #liczba zamówień na stronę
    change_list_template = 'admin/change_list1.html'

    
admin.site.register(Order, OrderAdmin)

class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ['order_user','product_name','price','quantity','created']
    search_fields = ['product_name']
    ordering = ['-created']

    def order_user(self,obj):
        return obj.order
    order_user.short_description = "Zamówienie"
    order_user.admin_order_field = 'order'

admin.site.register(OrderItem,OrderItemAdmin)
admin.site.site_header = 'Yakitori Panel Administracyjny'




