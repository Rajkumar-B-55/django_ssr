from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from order_svc.forms import OrderForm
from order_svc.models import Order
from product_svc.forms import ProductForm
from product_svc.models import Product
from users.forms import RegistrationForm_
from users.models import User


@login_required(login_url='login')
def index(request):
    product = Product.objects.all()
    product_count = product.count()
    order = Order.objects.all()
    order_count = order.count()
    customer = User.objects.all()
    customer_count = customer.count() - 1

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.customer = request.user
            obj.save()
            return redirect('dashboard_index')
    else:
        form = OrderForm()
    context = {
        'form': form,
        'order': order,
        'product': product,
        'product_count': product_count,
        'order_count': order_count,
        'customer_count': customer_count,
    }
    return render(request, 'index.html', context)


def users(request):
    form = RegistrationForm_()
    user_c = User.objects.all().exclude(role='admin')
    context = {
        'users': user_c,
        'form': form
    }
    return render(request, 'users/users.html', context)


def product(request):
    form = ProductForm()
    product_c = Product.objects.all()
    context = {
        'products': product_c,
        'form': form
    }
    return render(request, 'products/products.html', context)


def order(request):
    return render(request, 'orders/orders.html')
