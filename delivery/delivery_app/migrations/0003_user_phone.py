# Generated by Django 5.0.2 on 2024-02-26 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery_app', '0002_alter_product_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='phone',
            field=models.CharField(default='', max_length=100, verbose_name='Телефон'),
        ),
    ]
