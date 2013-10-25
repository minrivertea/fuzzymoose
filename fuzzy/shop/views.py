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

# APP
from utils import _render, _get_basket, _get_currency
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
    page = get_object_or_404(Page, slug=slug)
    return _render(request, 'page.html', locals())

def page_by_id(request, id):
    page = get_object_or_404(Page, pk=id)
    return HttpResponseRedirect(reverse('page', args=[page.slug]))

def basket(request, order=None, discount=None):
    
    try:
        order = get_object_or_404(Order, id=request.session['ORDER_ID'])
    except:
        pass
    
    if order:
        basket_items = order.items.all()
    else:
        basket_items = BasketItem.objects.filter(basket=_get_basket(request))
        
        
    # PRODUCTS
    total_price = float(0)
    for item in basket_items:
        total_price += float(item.get_price())
            
    # POSTAGE
    if RequestContext(request)['shopsettings'] != None:
        if total_price > RequestContext(request)['shopsettings'].postage_discount_threshold:
            postage_discount = True
        else:
            total_price += float(RequestContext(request)['shopsettings'].postage_price)
        
    # DISCOUNT
    if request.method == 'POST':
        form = DiscountForm(request.POST)
        if form.is_valid():
            
            discount = get_object_or_404(Discount, code=form.cleaned_data['discount_code'])
        
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
            _('Town or city'), _('State'), _('Post / ZIP code'), _('invalid'),
            )
            
        for k, v in post_values.iteritems():
            if v in initial_values:
                del post_values[k]
                
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
            
                    

            # CREATE AN ADDRESS OBJECT        
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
            
            # CREATE OR FIND THE ORDER
            try:
                order = get_object_or_404(Order, id=request.session['ORDER_ID'])
                if not order.hashkey:
                    order.hashkey = uuid.uuid1().hex
                    order.save()
                
            except:
                creation_args = {
                    'date_confirmed': datetime.now(),
                    'address': address,
                    'shopper': shopper,
                    'order_id': "TEMP",
                }
                order = Order.objects.create(**creation_args)
                order.save() # need to save it first, then give it an ID
                order.order_id = "TEA-00%s" % (order.id)
            
            # DO THEY HAVE A VALID DISCOUNT CODE?
            try: 
                discount = get_object_or_404(Discount, pk=request.session['DISCOUNT_ID'])
                order.discount = discount
            except:
                pass
            
            # UPDATE ORDER WITH THE BASKET ITEMS
            basket_items = BasketItem.objects.filter(basket=basket)
            for item in basket_items:
                order.items.add(item)
                
            order.save()
            request.session['ORDER_ID'] = order.id  
 
            # FINALLY! WE'RE DONE
            return HttpResponseRedirect(reverse('order_confirm')) 
        
        # IF THE FORM HAS ERRORS:
        else:
                         
             # LOAD EXISTING DATA
             email = request.POST['email']
             line_1 = request.POST['line_1']
             line_2 = request.POST['line_2']
             line_3 = request.POST['line_3']
             town_city = request.POST['town_city']
             postcode = request.POST['postcode']
             country = request.POST['country']
             first_name = request.POST['first_name']
             last_name = request.POST['last_name']
             
             try:
                 county = request.POST['county']
             except:
                 pass
             
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
                    
    # PRODUCTS
    total_price = 0
    for item in order.items.all():
        total_price += float(item.get_price())
        
    currency = _get_currency(request)
    
    # POSTAGE
    if RequestContext(request)['shopsettings'] != None:
        if total_price > RequestContext(request)['shopsettings'].postage_discount_threshold:
            postage_discount = True
        else:
            total_price += RequestContext(request)['shopsettings'].postage_price
        
    # DISCOUNT
    if order.discount:
        discount = float(total_price) * float(order.discount.discount_value)
        percent = order.discount.discount_value * 100
        total_price -= discount
    
    
    if request.method == 'POST':
        
        print "we're striping!"
        import stripe
        # Set your secret key: remember to change this to your live secret key in production # See your keys here https://manage.stripe.com/account 
        stripe.api_key = "sk_test_0rTa737wQgFgYRU7jB7FJfC6" 
        
        # Get the credit card details submitted by the form 
        token = request.POST['stripeToken'] 
        
        # Create the charge on Stripe's servers - this will charge the user's card 
        try: 
            charge = stripe.Charge.create( 
                amount=1000, # amount in cents, again 
                currency="gbp", 
                card=token, 
                description="payinguser@example.com" 
            ) 
            
            
            return HttpResponseRedirect(reverse('order_complete'))
             
        except stripe.CardError, e: 
           # The card has been declined 
           print "there was a big error"
           pass
           

    
        
    form = PayPalPaymentsForm()

    return _render(request, 'forms/order_confirm.html', locals())


def order_complete(request):
    
    
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

