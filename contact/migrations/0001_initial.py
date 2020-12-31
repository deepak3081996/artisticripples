# Generated by Django 3.0 on 2020-12-31 06:07

import contact.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('query_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(max_length=50, verbose_name='First Name')),
                ('last_name', models.CharField(max_length=50, verbose_name='Last Name')),
                ('email', models.EmailField(max_length=60, verbose_name='Email')),
                ('query', models.CharField(max_length=3000)),
                ('subject', models.CharField(max_length=100)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('query_date', models.DateTimeField(auto_now=True, verbose_name='Query Date')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=models.SET(contact.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='QueryUpdate',
            fields=[
                ('query_update_id', models.AutoField(primary_key=True, serialize=False)),
                ('reply', models.CharField(max_length=3000)),
                ('update_date', models.DateTimeField(auto_now=True, verbose_name='Update Date')),
                ('query', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contact.Query')),
                ('updated_query', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='contact.QueryUpdate')),
            ],
        ),
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('feedback_id', models.AutoField(primary_key=True, serialize=False)),
                ('first_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='First Name')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Last Name')),
                ('email', models.EmailField(blank=True, max_length=60, null=True, verbose_name='Email')),
                ('feedback', models.CharField(max_length=3000)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('feedback_date', models.DateTimeField(auto_now=True, verbose_name='Feedback Date')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=models.SET(contact.models.get_sentinel_user), to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
