from django.contrib.syndication.views import Feed
from blog.models import BlogEntry

class LatestEntriesFeed(Feed):
    title = "Chinese tea blog from the Min River Tea Farm"
    link = "/"
    description = "News and info about Chinese tea and our Chinese tea products."

    def items(self):
        return BlogEntry.objects.order_by('-date_added')[:10]

    def item_description(self, item):
        return item.summary
        
    def item_title(self, item):
        return item.title



