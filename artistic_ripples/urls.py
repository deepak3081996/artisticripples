from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
#sitemap
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import views
from .sitemaps import StaticViewSitemap
from mainapp.models import (
    Product, Quotation
)
from customer.models import Review

product_info_dict = {
    'queryset': Product.objects.all(),
    'date_field': 'pub_date',
}

quotation_info_dict = {
    'queryset': Quotation.objects.all(),
    'date_field': 'quotation_date',
}

review_info_dict = {
    'queryset': Review.objects.all(),
    'date_field': 'update_date',
}

sitemaps = {
    'static': StaticViewSitemap,
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('mainapp.urls')),
    path('contact/', include('contact.urls')),
    path('customer/', include('customer.urls')),
    # the sitemap
    path('sitemap.xml', sitemap,
         {'sitemaps': {
             **sitemaps,
             'product': GenericSitemap(product_info_dict, priority=0.6),
             'register_quotation': GenericSitemap(quotation_info_dict, priority=0.2),
             'reviews': GenericSitemap(review_info_dict, priority=0.2),
             }},
         name='django.contrib.sitemaps.views.sitemap'),
##    path('sitemap.xml', views.index, {'sitemaps': sitemaps}),
    path('sitemap-<section>.xml', views.sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
