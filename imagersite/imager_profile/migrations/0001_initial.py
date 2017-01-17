# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-17 02:51
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ImagerProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('camera_type', models.CharField(choices=[('pinhole', 'Pinhole'), ('fuji', 'Fuji'), ('nikon', 'Nikon'), ('canon', 'Canon'), ('sony', 'Sony'), ('hasselblad', 'Hasselblad'), ('iphone', 'iPhone'), ('analog slr', 'analog SLR'), ('analog rangefinder', 'analog rangefinder'), ('medium format', 'medium format'), ('funsnap', 'Funsnap')], default='pinhole', max_length=255)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('bio', models.TextField()),
                ('personal_website', models.URLField()),
                ('hireable', models.BooleanField(default=True)),
                ('travel_radius', models.DecimalField(decimal_places=1, max_digits=5)),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=128)),
                ('photography_type', models.CharField(choices=[('studio', 'Studio'), ('portraiture', 'Portraiture'), ('news_documentary', 'News/Documentary'), ('street photography', 'Street Photography'), ('weddings_events', 'Weddings and Events'), ('erotica', 'Erotica'), ('sports', 'Sports'), ('product', 'Product Photography')], default='selfies', max_length=255)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            managers=[
                ('active', django.db.models.manager.Manager()),
            ],
        ),
    ]
