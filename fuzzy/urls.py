from django.conf import settings
from django.conf.urls import patterns, include, url

from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from shop.utils import _internal_pages_list

from django.contrib import admin
admin.autodiscover()

from shop import views as shop_views

urlpatterns = patterns('',
    (r'^', include('fuzzy.shop.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^blog/', include('fuzzy.blog.urls')),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^ckeditor/', include('ckeditor.urls')),

    # important for the CKEDITOR page linking
    url(r'^view_internal_pages/$', _internal_pages_list, name="internal_pages_list"),

    
    url(r'^(?P<slug>[\w-]+)/(?P<product_slug>[\w-]+)/$', shop_views.product, name="product"),
    url(r'^(?P<slug>[\w-]+)/$', shop_views.category, name="category"),
    
    
)+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
