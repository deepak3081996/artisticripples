from django.contrib import admin
from django.contrib.auth.models import Group
from .models import (
    Product, ProductImage, Quotation
)

admin.site.site_header = "Artistic Ripples Admin dashboard"
# Register your models here.

##class InlineProductImage(admin.StackedInline):
##    model = ProductImage
##    extra = 1

class InlineProductImage(admin.TabularInline):
    model = ProductImage
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    inlines = [InlineProductImage]
    list_display = ["product_name", "category", "subcategory", "price"]
    list_filter = ["product_name", "category", "subcategory", "price"]

class QuotationAdmin(admin.ModelAdmin):
    list_display = ['quotation_id', 'content', 'full_name', 'added_on', 'author_comment', 'edit']
    list_display_links = ('edit',)
    ordering = ['quotation_id', ]

    class Meta:
        model = Quotation

admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(Quotation, QuotationAdmin)
admin.site.unregister(Group)
