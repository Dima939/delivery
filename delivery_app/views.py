from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import User, CartProduct, Product, Category
from .forms import LoginForm

login = False
uk = 0
bonuses = ''


def home(request):
    global login, uk
    if uk == 0:
        user = {}
    else:
        user = User.objects.get(id=uk)
    categories = Category.objects.all()
    return render(request, 'home.html', {'categories': categories, 'login': login, 'user': user})


def product_view(request, name):
    global login, uk
    if uk == 0:
        user = {}
    else:
        user = User.objects.get(id=uk)
    return render(request, 'product.html', {'product': Product.objects.get(name=name), 'login': login, 'user': user})


def products_list_view(request, pk):
    global login, uk
    if uk == 0:
        user = {}
    else:
        user = User.objects.get(id=uk)
    current_category = Category.objects.get(id=pk)
    return render(request, 'products_list.html', {'products': current_category.product_set.all(), 'login': login,
                                                  'user': user, 'category': current_category})


def login(request, choice):
    global login, uk
    form = LoginForm()
    if request.method == 'POST':
        users = User.objects.all()
        if choice == 'login':
            for user in users:
                if request.POST.get('email') == user.email and request.POST.get('phone') == user.phone\
                        and request.POST.get('password') == user.password:
                    uk = user.pk
                    login = True
                    for product in user.cartproduct_set.all():
                        product.delete()
                    return HttpResponseRedirect('/')
            return render(request, 'login.html', {'form': form, 'choice': choice})
        else:
            for user in users:
                if request.POST.get('email') == user.email or request.POST.get('phone') == user.phone:
                    break
            else:
                new_user = User(email=request.POST.get('email'), phone=request.POST.get('phone'),
                                password=request.POST.get('password'))
                new_user.save()
                uk = new_user.pk
                login = True
                return HttpResponseRedirect('/')
            return render(request, 'login.html', {'form': form, 'choice': choice})
    return render(request, 'login.html', {'form': form, 'choice': choice})


def exit(request):
    global login, uk
    user = User.objects.get(id=uk)
    for product in user.cartproduct_set.all():
        product.delete()
    login = False
    uk = 0
    return HttpResponseRedirect('/')


def profile_view(request):
    global uk
    change = False
    user = User.objects.get(id=uk)
    if request.method == 'POST':
        user.name = request.POST.get('name')
        user.address = request.POST.get('address')
        user.email = request.POST.get('email')
        user.phone = request.POST.get('phone')
        user.save()
        change = True
        return render(request, 'profile.html', {'user': user, 'change': change})
    return render(request, 'profile.html', {'user': user, 'change': change})


def cart_add(request, pk):
    user = User.objects.get(id=uk)
    product = Product.objects.get(id=pk)
    user.cartproduct_set.create(name=product.name, price=product.price, description=product.description,
                                image=product.image)
    return HttpResponseRedirect('/cart/')


def cart_view(request):
    global bonuses
    user = User.objects.get(id=uk)
    cart_products = user.cartproduct_set.all()
    cart_sum = 0
    for product in cart_products:
        cart_sum += product.price
    if len(str(cart_sum)) > 5:
        cart_sum = float(str(cart_sum)[:5])
    if request.method == 'POST':
        bonuses = request.POST.get('choice')
        return HttpResponseRedirect('/order/')
    return render(request, 'cart.html', {'products': cart_products, 'sum': cart_sum, 'user': user})


def delete(request, pk):
    product = CartProduct.objects.get(id=pk)
    product.delete()
    return HttpResponseRedirect('/cart/')


def order(request):
    user = User.objects.get(id=uk)
    cart_products = user.cartproduct_set.all()
    cart_sum = 0
    for product in cart_products:
        cart_sum += product.price
    result = cart_sum
    if bonuses == 'yes':
        if cart_sum - user.balance < 0:
            result = '0'
        else:
            result = cart_sum - user.balance

    if len(str(result)) > 5:
        result = float(str(result)[:5])

    if request.method == 'POST':
        user.address = request.POST.get('address')
        if bonuses == 'yes':
            if result == '0':
                user.balance -= cart_sum
                user.balance += 1.5
            else:
                user.balance = 1.5
        else:
            user.balance += 1.5
        user.save()
        for product in user.cartproduct_set.all():
            product.delete()
        return HttpResponseRedirect('/')
    return render(request, 'order.html', {'sum': result, 'user': user})
