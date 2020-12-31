from django.contrib import admin
from .models import Review

# Register your models here.
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['review_id', 'content', 'review_by', 'edit']
    list_display_links = ('edit',)
    ordering = ['user', ]

    class Meta:
        model = Review

admin.site.register(Review, ReviewAdmin)
