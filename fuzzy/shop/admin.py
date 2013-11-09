from models import *
from django.contrib import admin


class PhotoInline(admin.TabularInline):
    model = Photo
    # 'order' is taken care of by an AJAX thing. See menu-sort.js
    exclude = ('list_order',) 
    extra = 3
    
    class Media:
        js = (
                '/static/js/jquery-1.3.2.min.js',
                '/static/js/jquery-ui-1.7.1.custom.min.js',
                '/static/js/menu-sort.js',
        )

    def change_view(self, request, object_id, form_url='.', extra_context={}):
        object = self.model.objects.get(identifier=object_id)
        extra_context = {'photo': object,}
        return super(PhotoInline, self).change_view(request, object_id, form_url, extra_context)



class ProductAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("name",)}
    list_display = ('name', 'slug', 'is_active')
    list_filter = ('category',)
    inlines = [PhotoInline,]



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

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'list_thumbnail', 'list_order')
    

admin.site.register(Currency)
admin.site.register(ShopSettings)  
admin.site.register(Photo, PhotoAdmin)  
admin.site.register(Product, ProductAdmin)
admin.site.register(Address)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Shopper)
admin.site.register(Price, PriceAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(Page, PageAdmin)
admin.site.register(Review, ReviewAdmin)



