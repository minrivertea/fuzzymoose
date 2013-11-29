# DJANGO CORE
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import auth
from django.template import RequestContext
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.template.loader import render_to_string
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.utils import simplejson
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import ugettext as _
from django.utils.translation import get_language
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

import uuid
from datetime import datetime, timedelta


# APP
from utils import _render, _get_basket, _get_currency, _get_postage_cost
from models import *
from forms import *



def staff_required(function=None, redirect_field_name=auth.REDIRECT_FIELD_NAME):
    """ a wrapper on login_required that not only checks if you're logged in
    but also that you are logged in as staff. """
    def _checker(user):
        return user.is_authenticated() and user.is_staff
    actual_decorator = user_passes_test(
      _checker,
      redirect_field_name=redirect_field_name
   )
    if function:
        return actual_decorator(function)
    return actual_decorator




def home(request):    
    return _render(request, 'home.html', locals())
    
    
def category(request, slug):    
    category = get_object_or_404(Category, slug=slug)
    return _render(request, 'category.html', locals())
    
def category_by_id(request, id):
    category = get_object_or_404(Category, pk=id)
    return HttpResponseRedirect(reverse('category', args=[category.slug]))

def product(request, slug, product_slug):    
    product = get_object_or_404(Product, slug=product_slug)
    product.prices = Price.objects.filter(
        is_active=True,
        product=product,
        currency=RequestContext(request)['currency'],
    )
    return _render(request, 'product.html', locals())

def product_by_id(request, id):
    product = get_object_or_404(Product, pk=id)
    return HttpResponseRedirect(reverse('product', args=[product.slug]))

def page(request, slug):    
    promo_products = Product.objects.filter(is_active=True, category__isnull=False).order_by('?')[:2]
    page = get_object_or_404(Page, slug=slug)
    return _render(request, 'page.html', locals())

def page_by_id(request, id):
    page = get_object_or_404(Page, pk=id)
    return HttpResponseRedirect(reverse('page', args=[page.slug]))


def contact(request):
    
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            
            # send an email to the customer
            sender = settings.SITE_EMAIL
            recipient = [form.cleaned_data['your_email']]
            subject_line = 'Your message has been sent to %s' % settings.SITE_NAME
            content = render_to_string('emails/contact_customer.txt', locals(), RequestContext(request))
            msg = EmailMultiAlternatives(subject_line, content, sender, recipient)
            msg.send()
            
            # send an email to the admin
            sender = settings.SITE_EMAIL
            recipient = [settings.SITE_EMAIL]
            subject_line = '%s - a message just arrived from %s' % (settings.SITE_NAME, form.cleaned_data['your_email'])
            content = render_to_string('emails/contact_admin.txt', locals(), RequestContext(request))
            msg = EmailMultiAlternatives(subject_line, content, sender, recipient)
            msg.send()
            
            messages.add_message(request, messages.INFO, 'Your message has been sent!')
        
            return HttpResponseRedirect(reverse('contact'))
        else:
            form = ContactForm(request.POST)
    else:
        form = ContactForm()
    return _render(request, 'forms/contact.html', locals())

def basket(request, order=None, discount=None):
    
    try:
        order = get_object_or_404(Order, id=request.session['ORDER_ID'])
    except:
        delivery_date_form = DeliveryDateForm()
        pass
    
    basket_items = BasketItem.objects.filter(basket=_get_basket(request))
    
    
    # IS THERE A DELIVERY DATE
    delivery_date = None
    if order:
        delivery_date = order.preferred_delivery_date

    if delivery_date == None:
        try:
            delivery_date = request.session['DELIVERY_DATE']
        except:
            pass    
        
        
    # PRICES AND POSTAGE
    shopsettings = RequestContext(request)['shopsettings']
    total_price = float(0)
    for item in basket_items:                    
        item.total_price = item.get_price()
        total_price += float(item.total_price)

    postage_discount = False
    if shopsettings.flat_fee_postage_price:
        if total_price > shopsettings.postage_discount_threshold:
            postage_discount = True
        else:
            total_price += float(shopsettings.flat_fee_postage_price)
    
    else:
        for item in basket_items:
        
            if item.price.special_postage_price:
                total_price += float(item.quantity * item.price.special_postage_price)
                item.total_price = item.get_price() + (item.quantity * item.price.special_postage_price)
            
            else:
                total_price += float(item.quantity * shopsettings.standard_postage_price)
                item.total_price = item.get_price() + (item.quantity * shopsettings.standard_postage_price)
                

        
    # DISCOUNT
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            
            discount = get_object_or_404(Discount, code=form.cleaned_data['discount_code'])
            request.session['DISCOUNT_ID'] = discount.pk
        
        else:
            pass
    
    else:
        if order:
            if order.discount:
                discount = order.discount
    
    
    
    if request.GET.get('clear_discount'):
        discount = None
        if order:
            order.discount = None
            order.save()
            
    if discount:
        discount_amount = float(total_price) * float(discount.value)
        percent = discount.value * 100
        total_price -= discount_amount
    
    return _render(request, 'basket.html', locals())


def update_delivery_date(request):
    
    if request.method == 'POST':
        form = DeliveryDateForm(request.POST)
        if form.is_valid():
            
            # CHECK IF USER HAS AN ORDER ALREADY
            try:
                order = get_object_or_404(Order, id=request.session['ORDER_ID'])
                order.preferred_delivery_date = form.cleaned_data['preferred_delivery_date']
                order.save()
            except:
                request.session['DELIVERY_DATE'] = form.cleaned_data['preferred_delivery_date']
    
    return HttpResponseRedirect(reverse('basket'))    
    
    
# function for adding stuff to your basket
def add_to_basket(request, id):
    price = get_object_or_404(Price, pk=id)
    basket = _get_basket(request)
     
    try:
        item = get_object_or_404(BasketItem, basket=basket, price=price)
        item.quantity += 1
    except:
        item = BasketItem.objects.create(price=price, quantity=1, basket=basket)
    item.save()

    if request.is_ajax():
        message = '<div class="message"><div class="text"><h3>1 x %(item)s added to your basket! <a href="%(url)s">Checkout now &raquo;</a></h3></div></div>' % {
                    'item':item.price.product, 
                    'url': reverse('basket'),
            }
        basket_quantity = '%.2f' % float(RequestContext(request)['basket_amount'])
        data = {'message': message, 'basket_quantity': basket_quantity}
        json =  simplejson.dumps(data, cls=DjangoJSONEncoder)
        return HttpResponse(json)
    
    
    url = request.META.get('HTTP_REFERER','/')
    request.session['ADDED'] = item.id
    return HttpResponseRedirect(url)

# REMOVE AN ITEM COMPLETELY FROM YOUR BASKET
def remove_from_basket(request, id):
    basket_item = get_object_or_404(BasketItem, pk=id)
    basket_item.delete()
    return HttpResponseRedirect(reverse('basket'))


# REDUCE QUANTITY OF ITEM IN BASKET
def reduce_quantity(request, basket_item):        
    basket_item = get_object_or_404(BasketItem, pk=basket_item)
    if basket_item.quantity > 1:
        basket_item.quantity -= 1
        basket_item.save()
    else:
        pass
    
    return HttpResponseRedirect(reverse('basket'))


# INCREASE THE QUANTITY OF AN ITEM IN BASKET
def increase_quantity(request, basket_item):        
    basket_item = get_object_or_404(BasketItem, pk=basket_item)
    basket_item.quantity += 1
    basket_item.save()
    return HttpResponseRedirect(reverse('basket'))




def order_step_one(request, basket=None):
    
    basket = _get_basket(request)

    try:
        order = get_object_or_404(Order, id=request.session['ORDER_ID'])
        email = order.shopper.user.email
        line_1 = order.address.line_1
        line_2 = order.address.line_2
        line_3 = order.address.line_3
        town_city = order.address.town_city
        postcode = order.address.postcode
        county = order.address.county
        country = order.address.country
        first_name = order.shopper.user.first_name
        last_name = order.shopper.user.last_name
    except:
        order = None
    
    if not basket and not order:
        problem = "You don't have any items in your basket, so you can't process an order!"
        return _render(request, 'shop/order-problem.html', locals()) 
            

    if request.method == 'POST': 
        post_values = request.POST.copy()
        initial_values = (
            _('First name'), _('Last name'), _('Email address'),
            _('Your address...'), _(' ...address continued (optional)'),
            _('Town or city'), _('State'), _('Post / ZIP code'), _('--'),
            )
                        
        to_delete = []
        for k,v in post_values.iteritems():
            if k == 'csrfmiddlewaretoken': continue
            if v in initial_values:
                to_delete.append(k)
        
        for x in to_delete:
            del post_values[x]
                
        form = OrderStepOneForm(post_values)
        
        if form.is_valid(): 
            
            # FIRST, GET THE USER
            if request.user.is_authenticated():
                user = request.user
            else:
                try:
                    user = User.objects.get(email=form.cleaned_data['email'])
                    
                except:
                    creation_args = {
                            'username': form.cleaned_data['email'],
                            'email': form.cleaned_data['email'],
                            'password': uuid.uuid1().hex,
                    }
                    user = User.objects.create(**creation_args)
                    user.first_name = form.cleaned_data['first_name']
                    user.last_name = form.cleaned_data['last_name']
                    user.save()
                
                # SECRETLY LOG THE USER IN
                from django.contrib.auth import load_backend, login
                for backend in settings.AUTHENTICATION_BACKENDS:
                    if user == load_backend(backend).get_user(user.pk):
                        user.backend = backend
                if hasattr(user, 'backend'):
                    login(request, user)
            
            
            try:
                shopper = get_object_or_404(Shopper, user=user)
            except MultipleObjectsReturned:
                shopper = Shopper.objects.filter(user=user)[0]
            
            except:
                creation_args = {
                    'user': user,
                }
                shopper = Shopper.objects.create(**creation_args)
            
                    

            if form.cleaned_data['will_collect'] == False:# CREATE AN ADDRESS OBJECT        
                address = Address.objects.create(
                    shopper = shopper,
                    line_1 = form.cleaned_data['line_1'],
                    line_2 = form.cleaned_data['line_2'],
                    line_3 = form.cleaned_data['line_3'],
                    town_city = form.cleaned_data['town_city'],
                    postcode = form.cleaned_data['postcode'],
                    country = form.cleaned_data['country'],
                )
                
                try:
                    address.county = form.cleaned_data['county']
                    address.save()
                except:
                    pass
            else:
                address = None
            
            try:
                # TRY TO FIND AN EXISTING ORDER
                order = get_object_or_404(Order, id=request.session['ORDER_ID'])
                if not order.hashkey:
                    order.hashkey = uuid.uuid1().hex
                    order.save()
                                
                
            except:                
                # IF THERE'S NO ORDER, CREATE ONE NOW
                creation_args = {
                    'date_confirmed': datetime.now(),
                    'address': address,
                    'shopper': shopper,
                    'order_id': "TEMP",
                }
                order = Order.objects.create(**creation_args)
                order.save() # need to save it first, then give it an ID
                order.order_id = "ORDER-00%s" % (order.id)
                request.session['ORDER_ID'] = order.id
            
            # DO THEY HAVE A VALID DISCOUNT CODE?
            try: 
                discount = get_object_or_404(Discount, pk=request.session['DISCOUNT_ID'])
                order.discount = discount
            except:
                pass
            
            # DID THEY SPECIFY A DELIVERY DATE EARLIER?
            if not order.preferred_delivery_date:
                try:
                    order.preferred_delivery_date = request.session['DELIVERY_DATE']
                except:
                    pass
            
            if form.cleaned_data['will_collect'] == True:
                order.will_collect = True    
            
            # UPDATE ORDER WITH THE BASKET ITEMS
            basket_items = BasketItem.objects.filter(basket=basket)
            for item in basket_items:
                order.items.add(item)
            
            # SAVE THE ORDER, NOW ALL THE DATA IS THERE AND CORRECT    
            order.save()
 
            # FINALLY! WE'RE DONE
            return HttpResponseRedirect(reverse('order_confirm')) 
        
        # IF THE FORM HAS ERRORS:
        else:
                                                  
             # LOAD EXISTING DATA
             first_name = request.POST['first_name']
             last_name = request.POST['last_name']
             email = request.POST['email']
             line_1 = request.POST['line_1']
             line_2 = request.POST['line_2']
             line_3 = request.POST['line_3']
             town_city = request.POST['town_city']
             postcode = request.POST['postcode']
             country = request.POST['country']
             will_collect = request.POST['will_collect']
                          
             form = OrderStepOneForm(post_values)

        
    else:
        form = OrderStepOneForm()
    return _render(request, 'forms/order_step_one.html', locals())


def order_confirm(request):
    
    try:
        basket = get_object_or_404(Basket, id=request.session['BASKET_ID'])
    except KeyError:
        problem = _("You don't have any items in your basket, so you can't process an order!")
        return _render(request, 'shop/order-problem.html', locals())
        
    try:
        order = Order.objects.get(id=request.session['ORDER_ID'])
    except KeyError:
        problem = _("You don't have any items in your basket, so you can't process an order!")
        return _render(request, 'shop/order-problem.html', locals())
                    
                    
    currency = _get_currency(request)
    
    # PRICES AND POSTAGE
    shopsettings = RequestContext(request)['shopsettings']
    items = order.items.all()
    total_price = float(0)
    for item in items:                    
        item.total_price = item.get_price()
        total_price += float(item.total_price)

    if not order.will_collect:
        postage_discount = False
        if shopsettings.flat_fee_postage_price:
            if total_price > shopsettings.postage_discount_threshold:
                postage_discount = True
            else:
                total_price += float(shopsettings.flat_fee_postage_price)
        
        else:
            for item in items:
            
                if item.price.special_postage_price:
                    total_price += float(item.quantity * item.price.special_postage_price)
                    item.total_price = item.get_price() + (item.quantity * item.price.special_postage_price)
                
                else:
                    total_price += float(item.quantity * shopsettings.standard_postage_price)
                    item.total_price = item.get_price() + (item.quantity * shopsettings.standard_postage_price)
                    
            
        
    # DISCOUNT
    if order.discount:
        discount_amount = float(total_price) * float(order.discount.value)
        percent = order.discount.value * 100
        total_price -= discount_amount
    
    
    # FOR STRIPE, WE'LL CREATE A TOTAL VALUE IN PENNIES NOT POUNDS
    stripe_total_price = int(total_price * 100)
    if request.method == 'POST':
        
        import stripe
        # Set your secret key: remember to change this to your live secret key in production 
        # See your keys here https://manage.stripe.com/account 
        stripe.api_key = settings.STRIPE_API_SECRET_KEY 
        
        # Get the credit card details submitted by the form 
        token = request.POST['stripeToken'] 
        
        # Create the charge on Stripe's servers - this will charge the user's card 
        try: 
            charge = stripe.Charge.create( 
                amount=stripe_total_price, # amount in cents, again 
                currency="gbp", 
                card=token, 
                description="payinguser@example.com" 
            ) 
            
            return HttpResponseRedirect(reverse('order_complete', args=[order.hashkey]))
             
        except stripe.CardError, e: 
            # The card has been declined 
            print "there was a big error"
            pass
        
        except stripe.APIConnectionError:
            # operation timed out
            print "please try again"
               
        
    form = PayPalPaymentsForm()

    return _render(request, 'forms/order_confirm.html', locals())


def order_complete(request, hashkey=None):    
    
    # THIS IS WHERE STRIPE RETURNS US
    order = get_object_or_404(Order, haskey=hashkey)
    
    # FIRST, MARK THE ORDER AS 'PAID'
    order.date_paid = datetime.now()
    order.save()
    
    
    context = {
        'order': order,
        'SITE_NAME': settings.SITE_NAME,
        'site_name': settings.SITE_NAME,
        'SITE_URL': settings.SITE_URL,
        'site_url': settings.SITE_URL,
    }
    
    # SEND THE CUSTOMER AN EMAIL
    subject_line = 'Thanks for your order at %s' % settings.SITE_NAME
    recipient = order.shopper.user.email
    sender = settings.SITE_EMAIL
    content = render_to_string('emails/order_confirm_customer.txt', context)
    msg = EmailMultiAlternatives(subject_line, text_content, sender, recipient)
    msg.send()
    
    
    # SEND THE ADMINS AN EMAIL
    subject_line = 'NEW ORDER ON %s' % settings.SITE_NAME
    recipient = settings.SITE_EMAIL
    sender = settings.SITE_EMAIL
    content = render_to_string('emails/order_confirm_admin.txt', context)
    msg = EmailMultiAlternatives(subject_line, text_content, sender, recipient)
    msg.send()
    
    return _render(request, 'order_complete.html', locals())  


@csrf_exempt
@staff_required
def reorder_product_photos(request):

    if request.method == "POST":
        new_id_order = request.POST.getlist('ids')
        print new_id_order
    else:
        new_id_order = request.GET.getlist('ids')
        
    new_id_order = [int(x) for x in new_id_order]

    print new_id_order

    assert isinstance(new_id_order, list)
    assert new_id_order

    photos = []
    product = None
    for id_ in new_id_order:
        photo = get_object_or_404(Photo, id=id_)
        photos.append(photo)
        if product is None:
            product = photo.related_product
        else:
            assert product.id == photo.related_product.id, "different corefrocks"

    # MAKE SURE THE PHOTOS WE ARE REORDERING ARE THE SAME NUMBER AS IN THE DATABASE
    assert len(photos) == Photo.objects.filter(related_product=product).count()


    # SAVE THE NEW ORDER
    order = 1
    for p in photos:
        p.list_order = order
        p.save()
        order += 1

    # for the moment, let's assume that all frockphotos of this corefrock was used
    return HttpResponse("done")

