from django.db import models
from django.contrib.auth import get_user_model
from django.conf import settings
from datetime import timedelta

def get_sentinel_user():
    return get_user_model().objects.get_or_create(username='deleted')[0]

def get_anonymous_user():
    return get_user_model().objects.get_or_create(username='anonymous.user')[0]

class Feedback(models.Model):
    feedback_id = models.AutoField(primary_key=True)
    first_name = models.CharField(verbose_name="First Name", max_length=50, null=True, blank=True)
    last_name = models.CharField(verbose_name="Last Name", max_length=50, null=True, blank=True)
    email = models.EmailField(verbose_name="Email", max_length=60, null=True, blank=True)
    feedback = models.CharField(max_length=3000)    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        null=True, blank=True
    )
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    feedback_date = models.DateTimeField(verbose_name='Feedback Date', auto_now=True)

    @property
    def content(self):
        return self.feedback[:50]

    @property
    def full_name(self):
        return "{0} {1}".format((self.first_name if self.first_name else '-'),(self.last_name if self.last_name else '-'))

    @property
    def edit(self):
        return str('edit')


class Query(models.Model):
    query_id = models.AutoField(primary_key=True)
    first_name = models.CharField(verbose_name="First Name", max_length=50)
    last_name = models.CharField(verbose_name="Last Name", max_length=50)
    email = models.EmailField(verbose_name="Email", max_length=60)
    query = models.CharField(max_length=3000)
    subject = models.CharField(max_length=100)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user),
        null=True, blank=True
    )
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    query_date = models.DateTimeField(verbose_name='Query Date', auto_now=True)

    @property
    def content(self):
        return self.query[:50]

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def assigned_user(self):
        return self.user.username if self.user else "No user assigned"

    @property
    def edit(self):
        return str('edit')

    def __str__(self):
        return f"{self.email} \"{self.assigned_user}\""

class QueryUpdate(models.Model):
    query_update_id = models.AutoField(primary_key=True)
    reply = models.CharField(max_length=3000)
    update_date = models.DateTimeField(verbose_name='Update Date', auto_now=True)
    query = models.ForeignKey(Query, on_delete=models.CASCADE, null=True, blank=True)
    updated_query = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.query.subject)

    @property
    def query_detail(self):
        return f"{self.query.subject}-{self.query.query[:30]}" if self.query else "RE:"+self.updated_query.query_detail if self.updated_query else "Neither Query or Update Query is assigned."

    @property
    def assigned_user(self):
        return self.query.assigned_user if self.query else self.updated_query.assigned_user if self.updated_query else  "Neither Query or Update Query is assigned."

    @property
    def reply_content(self):
        return self.reply[:50]

    @property
    def edit(self):
        return str('edit')

    @property
    def updated_on(self):
        return str('')+str((self.update_date + timedelta(minutes=331)).strftime("%Y-%m-%d %H:%M:%S"))

    def __str__(self):
        return str(self.query_update_id)
