from django import template
from fuzzy.shop.models import Page, Product, Category
from django.shortcuts import get_object_or_404

import re

register = template.Library()

def get_new_url(match):
    m = match.group().split('/')[2]
    
    # TRY TO MATCH A PAGE
    if match.group().split('/')[1] == 'page':
        try:
            return get_object_or_404(Page, pk=m).get_absolute_url()
        except:
            pass
    
    # TRY TO MATCH A PRODUCT
    if match.group().split('/')[1] == 'product':
        try:
            return get_object_or_404(Product, pk=m).get_absolute_url()
        except:
            pass

    # TRY TO MATCH A CATEGORY
    if match.group().split('/')[1] == 'category':
        try:
            url = get_object_or_404(Category, pk=m).get_absolute_url()
            return url
        except:
            pass
    
    url = match.group()
    return url


@register.filter(name='convert_links')
def convert_links(text):
    """ This converts a link_by_id into a slug - it's a helper for WYSIWYG linking """
    url_pattern = re.compile(r'/\w+/\d+/')
    new_text = url_pattern.sub(get_new_url, text)
    return new_text
    






