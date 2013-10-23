from models import *
from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', 'category', 'is_active')
    list_filter = ('category',)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'parent', 'slug')
   
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'date_paid', 'shopper', )

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'is_published')
    
class PageAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')

class DiscountAdmin(admin.ModelAdmin):
    list_display = ('code', 'reminder', 'value')

class PriceAdmin(admin.ModelAdmin):
    list_display = ('product', 'price', 'is_active', 'currency')
    list_filter = ('is_active', 'currency')
    

admin.site.register(Currency)  
admin.site.register(Photo)  
admin.site.register(Product, ProductAdmin)
admin.site.register(Address)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Shopper)
admin.site.register(Price, PriceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Review, ReviewAdmin)



