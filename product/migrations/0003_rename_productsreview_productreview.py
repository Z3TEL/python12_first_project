# Generated by Django 3.2 on 2021-08-16 15:54

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('product', '0002_product_image'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ProductsReview',
            new_name='ProductReview',
        ),
    ]
