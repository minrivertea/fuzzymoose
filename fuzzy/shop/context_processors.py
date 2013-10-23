from django.conf import settings
from models import *
from utils import _get_country, _get_currency, _set_currency, _get_region

from django.contrib.sites.models import get_current_site




def common(request):
    context = {}
    context['paypal_return_url'] = settings.PAYPAL_RETURN_URL
    context['paypal_notify_url'] = settings.PAYPAL_NOTIFY_URL
    context['paypal_business_name'] = settings.PAYPAL_BUSINESS_NAME
    context['paypal_receiver_email'] = settings.PAYPAL_RECEIVER_EMAIL
    context['paypal_submit_url'] = settings.PAYPAL_SUBMIT_URL
    context['ga_is_on'] = settings.GA_IS_ON
    context['site_url'] = settings.SITE_URL # a full URL of the site
    context['analytics_id'] = settings.ANALYTICS_ID        
    context['site_name'] = settings.SITE_NAME # just the loose non-techy name of the site
    context['site_domain'] = settings.SITE_DOMAIN # the url without http://
    context['main_nav'] = Category.objects.filter(is_navigation_item=True).order_by('list_order')
    context['currency'] = _get_currency(request, currency_code='GBP')
    context['base_template'] = settings.BASE_TEMPLATE
    
    context['product_photo_large'] = settings.THUMBNAIL_PRODUCT_PHOTO_LARGE
    context['product_photo_medium'] = settings.THUMBNAIL_PRODUCT_PHOTO_MEDIUM
    context['product_photo_small'] = settings.THUMBNAIL_PRODUCT_PHOTO_SMALL


    # BASKET STUFF
    try:
        basket = Basket.objects.get(id=request.session['BASKET_ID'])
    except:
        basket = None
    
    basket_quantity = 0
    basket_amount = 0
    if basket:
        basket_items = BasketItem.objects.filter(basket=basket)
        for item in basket_items:
            basket_quantity += item.quantity
            basket_amount += float(item.get_price())
    
    context['basket_quantity'] = basket_quantity
    context['basket_amount'] = basket_amount       
    return context
    
  