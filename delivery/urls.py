from django.contrib import admin
from django.urls import path, re_path
from django.views.generic import TemplateView
from delivery_app import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home),
    re_path(r'category/(?P<pk>\d+)/', views.products_list_view),
    path('admin/', admin.site.urls),
    re_path(r'login/(?P<choice>\D+)/', views.login),
    path('home/', views.exit),
    path('profile/', views.profile_view),
    re_path(r'product/(?P<name>\D+)/', views.product_view),
    re_path(r'cart/(?P<pk>\d+)/', views.cart_add),
    path('cart/', views.cart_view),
    re_path(r'delete/(?P<pk>\d+)/', views.delete),
    path('order/', views.order),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
