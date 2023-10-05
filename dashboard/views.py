from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response

from order_svc.forms import OrderForm
from order_svc.models import Order
from product_svc.forms import ProductForm
from product_svc.models import Product
from users.decorators import allowed_users
from users.forms import RegistrationForm_
from users.models import User


@login_required(login_url='login')
def index(request):
    try:
        product = Product.objects.all()
        product_count = product.count()
        order = Order.objects.all()
        order_count = order.count()
        customer = User.objects.all()
        customer_count = customer.count() - 1
        user_week_count = user_count_by_week_view()
        user_monthly_count = user_count_by_month_view()

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
            'user_week_count': user_week_count,
            'user_monthly_count': user_monthly_count
        }
        return render(request, 'index.html', context)
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)})


@login_required(login_url='login')
def users(request):
    try:
        form = RegistrationForm_()
        user_c = User.objects.all().exclude(role='admin')
        context = {
            'users': user_c,
            'form': form
        }
        return render(request, 'users/users.html', context)
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)})


@login_required(login_url='login')
def product(request):
    try:
        form = ProductForm()
        product_c = Product.objects.all()
        context = {
            'products': product_c,
            'form': form
        }
        return render(request, 'products/products.html', context)
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)})


@login_required(login_url='login')
def order(request):
    try:
        order_dict = Order.objects.all()
        form = OrderForm()
        context = {
            'form': form,
            'orders': order_dict
        }
        return render(request, 'orders/orders.html', context)
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)})


def skip_admin():
    admin_user = User.objects.filter(role='admin').count()
    return admin_user


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def list_user_view(request):
    try:
        list_user = User.objects.all()
        users_list = [
            {'user_id': user.id,
             'first_name': user.first_name,
             'last_name': user.last_name,
             'email': user.email,
             'phone_number': user.phone_number,
             'is_active': user.is_active,
             'role': user.role,
             'date_joined': user.date_joined.strftime("%d-%m-%Y %H:%M"),
             'last_login': str(user.last_login)
             }
            for user in list_user
        ]
        return Response(data={"users": users_list}, status=status.HTTP_200_OK)

    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)}, status=status.HTTP_404_NOT_FOUND)


def user_count_by_week_view():
    try:
        user = User.objects.filter(date_joined__gte=timezone.now() - timezone.timedelta(weeks=1)).count()
        weekly_count = user - skip_admin()
        return weekly_count
    except Exception as e:
        return str(e)


def user_count_by_month_view():
    try:
        user = User.objects.filter(date_joined__gte=timezone.now() - timezone.timedelta(days=30)).count()
        monthly_count = user - skip_admin()
        return monthly_count
    except Exception as e:
        return str(e)
