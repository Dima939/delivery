from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class User(AbstractUser):
    bonus = models.FloatField(default=0)
    phone = models.CharField(max_length=100, verbose_name='Телефон', default='')


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Блюдо')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    photo = models.ImageField(upload_to='photos/', default=None, verbose_name='Изображение')
    price = models.FloatField()
    description = models.TextField(blank=True, verbose_name='Описание')
    structure = models.TextField(blank=True, verbose_name='Состав')
    cat = models.ForeignKey('Category', on_delete=models.CASCADE, related_name='products', blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE, related_name='products')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('product', kwargs={'prod_slug': self.slug})


class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Категория')
    slug = models.SlugField(max_length=255, unique=True, db_index=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('show_category', kwargs={'cat_slug': self.slug})

