from django.conf.urls.defaults import *
from django.utils.translation import ugettext_lazy as _

import views
import utils

urlpatterns = patterns('',

    url(r'^$', views.home, name="home"),
    
    # RELATED TO BASKET FUNCTIONS
    url(r'^basket/$', views.basket, name="basket"),
    url(r'^basket/add/(\w+)$', views.add_to_basket, name="add_to_basket"),
    url(r'^basket/reduce/(\w+)$', views.reduce_quantity, name="reduce_quantity"),
    url(r'^basket/increase/(\w+)$', views.increase_quantity, name="increase_quantity"),
    url(r'^basket/remove/(\w+)$', views.remove_from_basket, name="remove_from_basket"),
    
    # RELATES TO REORDERING THE PHOTOS
    url(r'^reorder-product-photos/$', views.reorder_product_photos, name="reorder_product_photos"),
    
    
    # GENERAL
    url(r'^contact/$', views.contact, name="contact"),
    #url(r'^reviews/$', views.reviews, name="reviews"),
    #url(r'^not-me/$', views.not_you, name="not_you"),
    url(r'^currency/$', utils._set_currency, name="set_currency"),    
    
    # ORDER PROCESS SPECIFIC 
    url(r'^order/step-one/$', views.order_step_one, name="order_step_one"),
    url(r'^order/confirm/$', views.order_confirm, name="order_confirm"),
    #url(r'^order/complete/fake/$', views.order_complete_fake, name="order_complete_fake"),
    url(r'^order/complete/$', views.order_complete, name="order_complete"),
    #url(r'^fake/checkout/(\w+)/$', views.fake_checkout, name="fake_checkout"),
    #url(r'^order/repeat/(?P<hash>[\w-]+)/$', views.order_repeat, name="order_repeat"),
    #url(r'^order/review/(?P<hash>[\w-]+)/$', views.review_order, name="review_order"),
    #url(r'^order/(?P<hash>[\w-]+)/friend/$', views.order_url_friend, name="order_url_friend"),
    #url(r'^order/(?P<hash>[\w-]+)/$', views.order_url, name="order_url"),

    url(r'^order/update-delivery-date/$', views.update_delivery_date, name="update_delivery_date"),
    
    # get objects by ID urls
    url(r'^page/(?P<slug>[\w-]+)/$', views.page, name="page"),
    url(r'^page/(\w+)/$', views.page_by_id, name="page_by_id"),
    url(r'^product/(\w+)/$', views.product_by_id, name="product_by_id"),
    url(r'^category/(\w+)/$', views.category_by_id, name="category_by_id"),
    
    
    
)

