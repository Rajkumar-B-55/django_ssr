from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response

from users.decorators import allowed_users
from .forms import ProductForm
from .models import Product


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def product_create(request):
    try:
        form = ProductForm(data=request.POST)
        if form.is_valid():
            form.save()
            product_name = form.cleaned_data.get('name')
            messages.success(request, f'{product_name} has been added')
            return redirect('dashboard_product')
        return render(request, 'products/products.html')
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)},
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required(login_url='login')
def products_get(request, pk):
    try:
        if pk:
            product = Product.objects.filter(pk=pk).first()
            if product is not None:
                prod_dict = {
                    'name': product.name,
                    'price': float(product.price),
                    'quantity': product.quantity,
                    'unit': product.unit,
                    'description': product.description,
                }
                return Response(prod_dict, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(data={'msg': 'mention product id'}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)},
                      status=status.HTTP_404_NOT_FOUND)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products_put(request, pk):
    try:
        product_instance = Product.objects.get(pk=pk)
        if request.method == 'POST':
            form = ProductForm(request.POST, instance=product_instance)
            if form.is_valid():
                form.save()
                return redirect('dashboard_product')
        else:
            form = ProductForm(instance=product_instance)
            context = {"form": form}
            return render(request, 'products/products_edit.html', context)

    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)},
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products_del(request, pk):
    try:
        product = get_object_or_404(Product, pk=pk)
        product_name = product.name
        product.delete()
        messages.success(request, f'{product_name} has been Deleted')
        return redirect('dashboard_product')
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)},
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)
