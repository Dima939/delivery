from django.contrib import admin
from .models import Product, Category, User
from django.contrib.auth.admin import UserAdmin


admin.site.register(User, UserAdmin)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'cat')
    list_display_links = ('name', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', )
    list_display_links = ('name', )
