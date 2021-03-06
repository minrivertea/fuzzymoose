from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.views.decorators.csrf import csrf_protect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404


from models import BlogEntry, Blogger
from fuzzy.shop.models import Product
from fuzzy.shop.utils import _get_products, _render



def index(request):
    objects = BlogEntry.objects.filter(
                is_draft=False, 
                title__isnull=False
                ).exclude(title__exact="None").order_by('-date_added')
      
    try:
        p = int(request.GET.get('page', '1'))
    except ValueError:
        p = 1
    
    paginator = Paginator(objects, 10) 
    # If page request (9999) is out of range, deliver last page of results.
    try:
        entries = paginator.page(p)
    except (EmptyPage, InvalidPage):
        entries = paginator.page(paginator.num_pages)
    
    promo_products = Product.objects.filter(
                is_active=True, 
                category__isnull=False
                ).order_by('?')[:2]
                           
    return _render(request, "blog/home.html", locals())
    
    
def blog_entry(request, slug):
    # TODO - THIS CAUSES 404 IF LANGUAGE IS SET TO EN AND SOMEONE REQUESTS A DE SLUG
    entry = get_object_or_404(BlogEntry, slug=slug)
    other_entries = BlogEntry.objects.filter(title__isnull=False).exclude(id=entry.id, title__exact="None").order_by('?')[:2]

    promo_products = Product.objects.filter(
                is_active=True, 
                category__isnull=False
                ).order_by('?')[:2]

    return _render(request, "blog/entry.html", locals())


def blog_by_id(request, id):
    blog = get_object_or_404(Blog, pk=id)
    return blog_entry(request, blog.slug)
  

def staff(request, slug):
    staff = get_object_or_404(Blogger, slug=slug)
    return _render(request, "blog/blogger.html", locals())