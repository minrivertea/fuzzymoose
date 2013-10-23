# DJANGO CORE
from django.db import models
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# APP
from countries import *

#class ShopSettings(models.Model):
#    postage_price = models.DecimalField()
#    postage_discount_threshold = models.DecimalField()
#    homepage_browser_title = models.CharField()
    
    
    

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True, null=True)
    parent = models.ForeignKey('Category', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    is_navigation_item = models.BooleanField(default=False)
    list_order = models.IntegerField(default=1)
    
    # SEO STUFF
    meta_description = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', args=[self.slug])
    
    def get_products(self):
        return Product.objects.filter(category=self, is_active=True)



class Product(models.Model):
    name = models.CharField(max_length=255)
    long_name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=100)
    short_description = models.TextField(blank=True, null=True)
    long_description = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    category = models.ForeignKey(Category)

    # SEO STUFF
    meta_description = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('product', args=[self.category.slug, self.slug])
    
    def get_prices(self, request):
        return Price.objects.filter(product=self, is_active=True)
    
    def get_photos(self):
        return Photo.objects.filter(related_product=self, is_published=True).order_by('list_order')
    
    def get_main_photo(self):
        return self.get_photos()[0]
    


class Review(models.Model):
    shopper = models.ForeignKey('Shopper')
    product = models.ForeignKey(Product)
    date_added = models.DateTimeField(default=datetime.now())
    original_text = models.TextField()
    edited_text = models.TextField()
    is_published = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s - %s" % (self.shopper, self.product)

class Photo(models.Model):
    image = models.ImageField(upload_to='photos')
    related_product = models.ForeignKey(Product, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(default=datetime.now())
    description = models.TextField(blank=True, null=True)
    list_order = models.IntegerField(default=1)




class Currency(models.Model):
    code = models.CharField(max_length=3)
    symbol = models.CharField(max_length=3)

    def __unicode__(self):
        return self.code
   
   
   
class Price(models.Model):
    product = models.ForeignKey(Product)
    price = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    currency = models.ForeignKey(Currency)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "%s (%s%s)" % (self.product, self.currency.symbol, self.price)
    
    

class Discount(models.Model):
    code = models.CharField(max_length=255)
    value = models.DecimalField(max_digits=5, decimal_places=2, 
        help_text="Use a decimal value - 0.1 is 10% off, 0.5 is 50% off, 1.0 is 100% discount")
    reminder = models.CharField(max_length=255, blank=True, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.code, self.reminder)
 
 
 
class Shopper(models.Model):
    user = models.ForeignKey(User)
    
    def __unicode__(self):
        return self.user
   
class Address(models.Model):
    shopper = models.ForeignKey(Shopper)
    line_1 = models.CharField(max_length=255, blank=True, null=True)
    line_2 = models.CharField(max_length=255, blank=True, null=True)
    line_3 = models.CharField(max_length=255, blank=True, null=True)
    town_city = models.CharField(max_length=255, blank=True, null=True)
    county = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=10, choices=COUNTRY_CHOICES, blank=True, null=True)
    postcode = models.CharField(max_length=255, blank=True, null=True)
    
    def __unicode__(self):
        return "%s (%s, %s)" % (self.shopper, self.line_1, self.postcode) 
    

class Page(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=100)
    summary = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    parent = models.ForeignKey('Page', blank=True, null=True)
    
    # SEO STUFF
    meta_description = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    
    def __unicode__(self):
        return self.name    

class Basket(models.Model):
    date_created = models.DateTimeField(default=datetime.now())
    def __unicode__(self):
        return self.id
    


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket)
    price = models.ForeignKey(Price)
    quantity = models.IntegerField()

    def __unicode__(self):
        return "%s x %s" % (self.price, self.quantity)
    
    def get_price(self):
        return (self.quantity * self.price.price)

class Order(models.Model):
    shopper = models.ForeignKey(Shopper)
    address = models.ForeignKey(Address, blank=True, null=True)
    items = models.ManyToManyField(BasketItem, blank=True, null=True)
    discount = models.ForeignKey(Discount, blank=True, null=True)
    order_id = models.CharField(max_length=50, blank=True, null=True)
    
    date_created = models.DateTimeField(default=datetime.now())
    date_confirmed = models.DateTimeField(blank=True, null=True)
    date_paid = models.DateTimeField(blank=True, null=True)
    
    def __unicode__(self):
        return self.order_id
    
    
    