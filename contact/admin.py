from django.contrib import admin
from .models import (
    Query, QueryUpdate, Feedback
)

# Register your models here.
class InlineQueryUpdate(admin.StackedInline):
    model = QueryUpdate
    extra = 1

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['feedback_id', 'email', 'full_name', 'content', 'edit']
    list_display_links = ('edit', )
    ordering = ['-feedback_id', ]
    
class QueryAdmin(admin.ModelAdmin):
    inlines = [InlineQueryUpdate]
    list_display = ['email', 'full_name', 'subject', 'content', 'assigned_user', 'edit']
    list_display_links = ('edit', )
    ordering = ['email', ]

    class Meta:
        model = Query

class QueryUpdateAdmin(admin.ModelAdmin):
    inlines = [InlineQueryUpdate]
    list_display = ['query_detail', 'reply_content', 'assigned_user', 'update_date', 'edit']
    list_display_links = ('edit', )
    ordering = ['update_date']

admin.site.register(Feedback, FeedbackAdmin)    
admin.site.register(Query, QueryAdmin)
admin.site.register(QueryUpdate, QueryUpdateAdmin)
