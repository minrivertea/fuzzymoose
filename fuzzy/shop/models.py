# DJANGO CORE
from django.db import models
from django.conf import settings
from datetime import datetime
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import get_object_or_404


import uuid

from ckeditor.fields import RichTextField
from sorl.thumbnail import get_thumbnail

from paintstore.fields import ColorPickerField


# APP
from countries import *


class ShopSettings(models.Model):
    
    flat_fee_postage_price = models.DecimalField(max_digits=8, decimal_places=2, 
        null=True, blank=True, 
        help_text="If there's a single postage fee, regardless of how many items, fill it in here. eg. 2.99")
    standard_postage_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="If there's a standard per-item postage fee, fill it in here.eg. 1.99")
    postage_discount_threshold = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True, 
        help_text="Is postage free if the customer orders more than &pound;XX? Put in that value here.")
    google_analytics_script = models.TextField(blank=True, null=True,
        help_text="Google gives you a script to place on the page that tracks visits - paste the whole thing here in its entirety (including the &lt;script&gt; tags!)")
    
    # FILES
    logo = models.ImageField(upload_to='global_files', blank=True, null=True,
        help_text="Upload a PNG file with transparency for best results. Less than 200px tall and 400px wide is probably best.")
    main_background_image = models.ImageField(upload_to='global_files', blank=True, null=True)
    main_background_color = ColorPickerField(blank=True, null=True)
    footer_background_image = models.ImageField(upload_to='global_files', blank=True, null=True)
    footer_background_color = ColorPickerField(blank=True, null=True)
    footer_logo = models.ImageField(upload_to='global_files', blank=True, null=True)
    
    # ALLOWS CHANGING OF VARIOUS COLOURS
    extra_css = models.TextField(blank=True, null=True, 
        help_text="Add in any extra css rules here and they will override the standard CSS on every page.")
    link_color = ColorPickerField(blank=True, null=True)
    
    # HOMEPAGE RELATED STUFF
    homepage_browser_title = models.CharField(max_length=255, blank=True, null=True)
    homepage_top_text = models.TextField(blank=True, null=True,
        help_text="The intro text at the top of the homepage.")
    homepage_mugshot = models.ImageField(upload_to="homepage", blank=True, null=True, 
        help_text="A little mugshot that appears next to the introduction text on the homepage. 90x120px")
    homepage_big_text = models.TextField(blank=True, null=True,
        help_text="The large text in the middle of the homepage")
    homepage_image = models.ImageField(upload_to="homepage", blank=True, null=True,
        help_text="The full-width image at the bottom of the homepage. Make sure it's at least 1000px wide")
    homepage_image_text = RichTextField(blank=True, null=True,
        help_text="The intro text at the top of the homepage.")
    
    def __unicode__(self):
        return "Shop Settings: %s" % self.id
    
    
    

class Category(models.Model):
    name = models.CharField(max_length=255, help_text="The name a customer will see on the website")
    slug = models.SlugField(max_length=100,
        help_text="This forms part of the URL. Use lowercase letters, no special characters and no spaces!")
    description = RichTextField(blank=True, null=True,
        help_text="A short description that appears at the top of the Category listing page. HTML is OK")
    parent = models.ForeignKey('Category', blank=True, null=True,
        help_text="Is this a subcategory of something else? If not, leave blank.")
    is_active = models.BooleanField(default=False,
        help_text="If ticked, it will appear on the public site")
    is_navigation_item = models.BooleanField(default=False,
        help_text="If ticked, it will appear as a navigation item in the main nav.")
    list_order = models.IntegerField(default=1,
        help_text="This defines the order it appears in the navigation. Lower numbers means further left.")
    
    # SEO STUFF
    meta_description = models.TextField(blank=True, null=True,
        help_text="A description used in the code of the page that helps Google results.")
    meta_title = models.CharField(max_length=255, blank=True, null=True,
        help_text="A custom page title that you can provide for search engines")
    meta_keywords = models.CharField(max_length=255, blank=True, null=True, 
        help_text="A list of keywords for the page. Not super-important.")

    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('category', args=[self.slug])
    
    def get_products(self):
        return Product.objects.filter(category=self, is_active=True)
    
    # IMPORTANT FOR INTERNAL LINKING VIA CKEDITOR
    def get_url_by_id(self):
        url = reverse('category_by_id', args=[self.id])
        return url



class Product(models.Model):
    name = models.CharField(max_length=255)
    long_name = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=100)
    short_description = models.TextField(blank=True, null=True)
    long_description = RichTextField(blank=True, null=True)
    content = RichTextField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    category = models.ManyToManyField(Category, blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    mixed_box = models.BooleanField(default=False, 
        help_text="Tick this and the product will allow customers to choose multiple flavours to go in this box")
    mixed_box_number = models.IntegerField(blank=True, null=True,
        help_text="How many choices does the customer get? 2 or more.")

    in_stock = models.BooleanField(default=True, 
        help_text="Deselect this and the product will be marked as 'Out of Stock' on the website.")

    # SEO STUFF
    meta_description = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        
        if self.category.all():
            main_cat = self.category.all()[0]          
            return reverse('product', args=[main_cat.slug, self.slug])
        else:
            return None
    
    # IMPORTANT FOR INTERNAL LINKING VIA CKEDITOR
    def get_url_by_id(self):
        url = reverse('product_by_id', args=[self.id])
        return url
    
    def get_reviews(self):
        return Review.objects.filter(is_published=True, product=self)[:2]
    
    def get_prices(self):
        prices = Price.objects.filter(product=self, is_active=True)
        return prices
    
    def get_photos(self):
        return Photo.objects.filter(related_product=self, is_published=True)
            
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
        return "%s - %s" % (self.shopper.user.email, self.product)

class Photo(models.Model):
    class Meta:
        ordering = ('list_order',)
    
    image = models.ImageField(upload_to='photos', blank=True, null=True)
    related_product = models.ForeignKey(Product, blank=True, null=True)
    is_published = models.BooleanField(default=False)
    date_uploaded = models.DateTimeField(default=datetime.now())
    description = models.TextField(blank=True, null=True)
    list_order = models.IntegerField(default=1)
    
    def move_up(self):
        """ change the order of this Photo to be one notch higher """
        photos = Photo.objects.filter(related_product=self.related_product).order_by('list_order')
        new_order = []
        position = 0
        for photo in photos:
            if photo.id == self.id:
                new_order.insert(position - 1, photo)
            else:
                new_order.insert(position, photo)
            position += 1
        for i, photo in enumerate(new_order):
            if photo.order != i:
                photo.order = i
                photo.save()

    def move_down(self):
        """ change the order of this Photo to be one notch higher """
        new_order = list(Photo.objects.filter(related_product=self.related_product).order_by('list_order'))
        new_index = new_order.index(self) + 1
        new_order.remove(self)
        new_order.insert(new_index, self)

        for i, photo in enumerate(new_order):
            if photo.order != i:
                photo.order = i
                photo.save()
    
    def list_thumbnail(self):
        try:
            im = get_thumbnail(self.image, '60x60', crop='center', quality=99)
            html = '<img src="%s" alt="False" />' % im.url
        except:
            html = ''
        
        return html
    list_thumbnail.allow_tags = True
    




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
    out_of_stock = models.BooleanField(default=False, 
        help_text="Tick this to mark an item as 'Out of Stock' on the website") # deprecated
    special_postage_price = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True,
        help_text="If this item has special pricing (above the normal rate) then add the full postage cost here (eg. if this will cost &pound;4 to post, type in 4.00 here)")
    
    def __unicode__(self):
        return "%s (%s%s)" % (self.product, self.price, self.currency.code)
    
    

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
        return self.user.email
   
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
    content = RichTextField(blank=True, null=True)
    is_published = models.BooleanField(default=False)
    parent = models.ForeignKey('Page', blank=True, null=True)
    
    # NAVIGATION
    is_top_navigation = models.BooleanField()
    list_order = models.IntegerField(default=0)
    
    # FOOTER
    is_footer_link = models.BooleanField()
    
    # SEO STUFF
    meta_description = models.TextField(blank=True, null=True)
    meta_title = models.CharField(max_length=255, blank=True, null=True)
    meta_keywords = models.CharField(max_length=255, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('page', args=[self.slug])
    
    # IMPORTANT FOR INTERNAL LINKING VIA CKEDITOR
    def get_url_by_id(self):
        return reverse('page_by_id', args=[self.id])
        

class Basket(models.Model):
    date_created = models.DateTimeField(default=datetime.now())
    
    def __unicode__(self):
        return self.id
    
    def get_items(self):
        return BasketItem.objects.filter(basket=self)
    


class BasketItem(models.Model):
    basket = models.ForeignKey(Basket)
    price = models.ForeignKey(Price)
    quantity = models.IntegerField()
    
    # specific for mixed boxes
    mixed_box_choices = models.ManyToManyField(Product, blank=True, null=True)

    def __unicode__(self):
        return "%s x %s" % (self.price, self.quantity)
    
    def get_price(self):                
        return (self.quantity * self.price.price)

class Order(models.Model):
    hashkey = models.CharField(max_length=100, blank=True, null=True)
    shopper = models.ForeignKey(Shopper)
    address = models.ForeignKey(Address, blank=True, null=True)
    items = models.ManyToManyField(BasketItem, blank=True, null=True)
    discount = models.ForeignKey(Discount, blank=True, null=True)
    order_id = models.CharField(max_length=50, blank=True, null=True)
    
    date_created = models.DateTimeField(default=datetime.now())
    date_confirmed = models.DateTimeField(blank=True, null=True)
    date_paid = models.DateTimeField(blank=True, null=True)
    
    preferred_delivery_date = models.DateTimeField(blank=True, null=True)
    will_collect = models.BooleanField(default=False)
    
    final_amount_paid = models.CharField(max_length=200, blank=True, null=True)
        
    def __unicode__(self):
        return self.order_id
        
    def save(self, *args, **kwargs):
        if not self.hashkey:
            self.hashkey = uuid.uuid1().hex
        super(Order, self).save(*args, **kwargs)
    
    
    def get_currency(self):
        # LAZY, BECAUSE SITE ONLY HAS GBP FOR NOW AND NEAR FUTURE
        return get_object_or_404(Currency, code='GBP')

    
    