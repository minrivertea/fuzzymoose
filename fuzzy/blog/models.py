from django.db import models
from fuzzy.shop.models import Page

from ckeditor.fields import RichTextField

class BlogEntry(models.Model):
    title = models.CharField(max_length=200, 
        help_text="")
    slug = models.SlugField(max_length=80)
    blogger = models.ForeignKey('Blogger', blank=True, null=True)
    promo_image = models.ImageField(upload_to='images/blog-photos', blank=True, null=True)
    date_added = models.DateField()
    is_draft = models.BooleanField(default=True)
    is_promoted = models.BooleanField(default=False)
    summary = models.CharField(max_length=200)
    
    content = RichTextField()
    comments_require_captcha = models.BooleanField(default=False, 
        help_text="If ticked, visitors will need to fill in captchas before commenting")
    comments_closed = models.BooleanField(default=False, 
        help_text="If ticked, visitors will not be able to comment on this entry")
    
    def __unicode__(self):
        return self.slug
        
    def get_absolute_url(self):
        return "/blog/%s/" % self.slug # important! do not change (for feeds)

    def get_url_by_id(self):
        url = "/blog/%s/" % self.id
        return url
     
    def get_content(self):
        return self.summary


class Blogger(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    profile_photo = models.ImageField(upload_to='images/bloggers')
    page = models.ForeignKey(Page, blank=True, null=True)
    
    def __unicode__(self):
        return self.name
       
        
