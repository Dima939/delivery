from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('product/<slug:prod_slug>/', views.ShowProduct.as_view(), name='product'),
    path('category/<slug:cat_slug>/', views.ShowCategory.as_view(), name='show_category'),
    path('login/', views.LoginUser.as_view(), name='login'),
    path('register/', views.RegisterUser.as_view(), name='register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.ProfileUser.as_view(), name='profile'),
    path('cart/', views.ShowCart.as_view(), name='cart'),
    path('add_product/<slug:prod_slug>/', views.add_product, name='add_product'),
    path('delete_product/<slug:prod_slug>', views.delete_product, name='delete_product'),
    path('order/', views.order, name='order'),
]
