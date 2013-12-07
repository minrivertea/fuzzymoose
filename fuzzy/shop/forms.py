from django import forms
from django.conf import settings
from django.forms import ModelForm
from django.contrib.auth.models import User

from captcha.fields import CaptchaField

from models import Address, Order, Discount, Shopper, Product, BasketItem, Currency, Price
from countries import ALL_COUNTRIES, COUNTRY_CHOICES, US_STATES


 
class AddressAddForm(ModelForm): 
    class Meta:
        model = Address
        exclude = ('owner', 'is_preferred',)
        
            
# handles the submission of their personal details during the order process
class OrderStepOneForm(forms.Form):
    email = forms.EmailField(required=True, 
        error_messages={'required': '* Please give an email address', 'invalid': '* Please enter a valid e-mail address.'})
    first_name = forms.CharField(max_length=200, required=True, error_messages={'required': '* Please give your first name'})
    last_name = forms.CharField(max_length=200, required=True, error_messages={'required': '* Please give your last name'})
    line_1 = forms.CharField(max_length=200, required=False)
    line_2 = forms.CharField(max_length=200, required=False)
    line_3 = forms.CharField(max_length=200, required=False)
    town_city = forms.CharField(max_length=200, required=False, error_messages={'required': '* Please provide a town or city name'})
    postcode = forms.CharField(max_length=200, required=False)
    country = forms.ChoiceField(required=True, choices=COUNTRY_CHOICES)
    will_collect = forms.BooleanField(required=False)
    
    def clean(self):
        data = self.cleaned_data
        if data.get('will_collect') == True:
            data['line_1'] = 'a'
            data['line_2'] = 'a'
            data['line_3'] = 'a'
            data['town_city'] = 'a'
            data['postcode'] = 'a'
            data['country'] = 'UK'
        
        else:
            if not data['postcode'] or not data['country'] or not data['line_1']:
                raise forms.ValidationError("You must provide at least the first line of your address, your postcode and country.")
            
        return data
    

class DiscountForm(forms.Form):
    discount_code = forms.CharField(required=True)
    
    def clean_discount_code(self):
        data = self.cleaned_data['discount_code']
        try:
            discount_object = Discount.objects.get(code=data)
            return data
        except:
            raise forms.ValidationError("Sorry, that's not a valid discount code!")
        return data



# handles the contact us form
class ContactForm(forms.Form):
    your_name = forms.CharField(required=True)
    your_email = forms.EmailField(required=True, error_messages={'required': 'Please enter a valid email address'})
    your_message = forms.CharField(widget=forms.Textarea, required=False)
    captcha = CaptchaField()




class UpdateProfileForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    email = forms.EmailField(required=False, error_messages={'required': 'Please enter a valid email address'})
  
# the form for submitting a tell-a-friend email address
class TellAFriendForm(forms.Form):
    recipient = forms.EmailField(required=True, error_messages={'required': '* You must give an email address for your friend'})
    sender = forms.EmailField(required=True, error_messages={'required': '* You must give your own email address'})
    message = forms.CharField(required=False, widget=forms.Textarea)

# after the user has finished ordering, handles submission of their twitter username
class SubmitTwitterForm(forms.Form):
    twitter_username = forms.CharField()
    
# handles the testimonials or reviews of a particular tea (views.review)
class ReviewForm(forms.Form):
    text = forms.CharField(required=True, widget=forms.Textarea)
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)
    email = forms.EmailField(required=True, error_messages={'required': '* You must give a valid email address'})


class ReviewOrderForm(forms.Form):
    words = forms.CharField(required=True, widget=forms.Textarea)
    product = forms.CharField(required=True)

class NotifyForm(forms.Form):
    email = forms.EmailField(required=True, error_messages={'required': 'Please enter a valid email address'})
    country = forms.ChoiceField(required=False, choices=ALL_COUNTRIES)

class SelectWishlistItemsForm(forms.Form):
    hashkey = forms.CharField()
    items = forms.CharField(required=False)


class DeliveryDateForm(ModelForm):
    class Meta:
        model = Order
        fields = ('preferred_delivery_date',)        

class WishlistSubmitEmailForm(forms.Form):
    email = forms.CharField()
    order = forms.CharField()    
   
    
class CreateSendEmailForm(forms.Form):
    subject_line = forms.CharField(required=True)
    content = forms.CharField(required=True, widget=forms.Textarea)

