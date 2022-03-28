from django.db import models


class User(models.Model):
    name = models.CharField(max_length=15, default='')
    address = models.CharField(max_length=50, default='')
    balance = models.FloatField(default=0.00)
    email = models.EmailField()
    phone = models.CharField(max_length=13)
    password = models.CharField(max_length=15)

    def __str__(self):
        return self.email


class CartProduct(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='images', blank=True, null=True)


class Category(models.Model):
    name = models.CharField(max_length=15)
    image = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    price = models.FloatField()
    description = models.TextField()
    image = models.ImageField(upload_to='images', blank=True, null=True)

    def __str__(self):
        return self.name
