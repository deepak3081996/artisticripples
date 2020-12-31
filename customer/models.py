from django.db import models
from django.conf import settings
from mainapp.models import Product
from datetime import timedelta
#for sitemap
from django.urls import reverse
from django.contrib.sitemaps import ping_google


class Review(models.Model):
    review_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.DO_NOTHING,
        null=True, blank=True
    )
    review_content = models.CharField(max_length=3000, verbose_name="Review")
    previous_review = models.ForeignKey('self', verbose_name="Previous Review",
                                       on_delete=models.CASCADE,
                                       null=True, blank=True
                                       )
    product = models.ForeignKey(Product, on_delete=models.DO_NOTHING,
                                null=True, blank=True
                                )
    update_date = models.DateTimeField(verbose_name='Update Date', auto_now=True)

    def __str__(self):
        return str(self.review_content)

    @property
    def content(self):
        return self.review_content[:50]

    @property
    def review_by(self):
        return self.user.username

    @property
    def updated_on(self):
        return str('')+str((self.update_date + timedelta(minutes=331)).strftime("%Y-%m-%d %H:%M:%S"))

    @property
    def edit(self):
        return str('edit')

    #for sitemap
    def get_absolute_url(self):
        return reverse('review', kwargs={'product_id':self.product.product_id}) if self.product else reverse('reply', kwargs={'review_id':self.review_id})

    def save(self, force_insert=False, force_update=False):
        super().save(force_insert, force_update)
        try:
            ping_google()
        except Exception:
            # Bare 'except' because we could get a variety
            # of HTTP-related exceptions.
            pass

