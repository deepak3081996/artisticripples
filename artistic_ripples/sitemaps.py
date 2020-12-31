from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'daily'

    def items(self):
        return ['feedback', 'query', 'querysuccess', 'tracking',
                'registerCustomer', 'login', 'logout', 'changePassword',
                'index', 'about', 'ProductView', 'quotationtracking', 'gallery']

    def location(self, item):
        return reverse(item)
