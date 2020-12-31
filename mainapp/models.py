from django.db import models
from django.conf import settings
from datetime import timedelta
#for sitemap
from django.urls import reverse
from django.contrib.sitemaps import ping_google

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]


class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    desc = models.CharField(max_length=300)
    price = models.IntegerField(default=0)
    image = models.ImageField(upload_to="shop/images", default="")
    pub_date = models.DateField()

    def __str__(self):
        return self.product_name

    #for sitemap
    def get_absolute_url(self):
        return reverse('productDetail', kwargs={'pk':self.product_id})

    def save(self, force_insert=False, force_update=False):
        super().save(force_insert, force_update)
        try:
            ping_google()
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass

class ProductImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    img_file = models.ImageField(upload_to="shop/images", default="")
    upload_date = models.DateTimeField(verbose_name='Upload Date', auto_now=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.img_file)

class Quotation(models.Model):
    quotation_id = models.AutoField(primary_key=True)
    first_name = models.CharField(verbose_name="First Name", max_length=50)
    last_name = models.CharField(verbose_name="Last Name", max_length=50)
    email = models.EmailField(verbose_name="Email", max_length=60)
    quotation = models.CharField(max_length=3000, blank=True)
    customization = models.CharField(max_length=3000)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        null=True, blank=True
    )
    product = models.ForeignKey(Product,on_delete=models.DO_NOTHING, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    quotation_date = models.DateTimeField(verbose_name='Quotation Date', auto_now=True)
    author_comment = models.CharField(max_length=3000, null=True, blank=True)

    @property
    def content(self):
        return self.quotation[:50]

    @property
    def full_name(self):
        return "{0} {1}".format((self.first_name if self.first_name else '-'),(self.last_name if self.last_name else '-'))

    @property
    def added_on(self):
        return str('')+str((self.quotation_date + timedelta(minutes=331)).strftime("%Y-%m-%d %H:%M:%S"))

    @property
    def edit(self):
        return str('edit')

    #for sitemap
    def get_absolute_url(self):
        return reverse('registerQuotation', kwargs={'product_id':self.product_id})

    def save(self, force_insert=False, force_update=False):
        super().save(force_insert, force_update)
        try:
            ping_google()
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass
    
    
