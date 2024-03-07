from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from .models import Product, Category
from .forms import LoginUserForm, RegisterUserForm, ProfileUserForm, OrderForm


class Home(ListView):
    template_name = 'delivery_app/home.html'
    context_object_name = 'products'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница'
        cats = Category.objects.all()
        context['cats'] = cats
        cats_list = []
        for cat in cats:
            products = Product.objects.filter(cat=cat)
            if products:
                cats_list.append(cat)
        context['cats_list'] = cats_list
        return context

    def get_queryset(self):
        return Product.objects.all()


class ShowProduct(DetailView):
    model = Product
    template_name = 'delivery_app/product.html'
    slug_url_kwarg = 'prod_slug'
    context_object_name = 'product'

    def get_object(self, queryset=None):
        return get_object_or_404(Product.objects.all(), slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['product'].name
        return context


class ShowCategory(ListView):
    template_name = 'delivery_app/show_category.html'
    context_object_name = 'products'
    allow_empty = False

    def get_queryset(self):
        return Product.objects.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = context['products'][0].cat.name
        cats = Category.objects.all()
        context['cats'] = cats
        cats_list = []
        for cat in cats:
            products = Product.objects.filter(cat=cat)
            if products:
                cats_list.append(cat)
        context['cats_list'] = cats_list
        return context


class ShowCart(ListView):
    template_name = 'delivery_app/cart.html'
    context_object_name = 'products'

    def get_queryset(self):
        return Product.objects.filter(user=self.request.user).select_related('user')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Корзина'
        products = Product.objects.filter(user=self.request.user)
        sum = 0
        for product in products:
            sum += product.price
        context['sum'] = sum
        return context


@login_required
def add_product(request, prod_slug):
    current_product = Product.objects.get(slug=prod_slug)
    user = request.user

    new_product = Product(name=current_product.name, photo=current_product.photo,
                          price=current_product.price, description=current_product.description,
                          structure=current_product.structure, user=user)
    index = 0
    while True:
        try:
            new_product.slug = current_product.slug + str(index)
            new_product.save()
            break
        except:
            index += 1

    return HttpResponseRedirect('/cart/')


def delete_product(request, prod_slug):
    product = get_object_or_404(Product.objects.all(), slug=prod_slug)
    product.delete()
    return HttpResponseRedirect('/cart/')


def order(request):
    user = request.user
    products = Product.objects.filter(user=user)
    sum = 0
    for product in products:
        sum += product.price

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            current_sum = sum
            if form.cleaned_data['is_bonus']:
                sum -= user.bonus
                user.bonus = 0
                user.save()

            user.bonus += current_sum/10
            user.save()

            for product in products:
                product.delete()

            data = {
                'title': 'Заказ Оформлен',
                'sum': sum,
            }
            return render(request, 'delivery_app/order_done.html', context=data)
    else:
        form = OrderForm()
        data = {
            'title': 'Оформление заказа',
            'sum': sum,
            'form': form
        }
        return render(request, 'delivery_app/order.html', context=data)


class LoginUser(LoginView):
    form_class = LoginUserForm
    template_name = 'delivery_app/login.html'
    extra_context = {'title': 'Авторизация'}

    def get_success_url(self):
        return reverse_lazy('home')


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = 'delivery_app/register.html'
    extra_context = {'title': 'Регистрация'}
    success_url = reverse_lazy('home')


class ProfileUser(LoginRequiredMixin, UpdateView):
    model = get_user_model()
    form_class = ProfileUserForm
    template_name = 'delivery_app/profile.html'
    extra_context = {'title': 'Профиль пользователя'}

    def get_success_url(self):
        return reverse_lazy('profile')

    def get_object(self, queryset=None):
        return self.request.user
