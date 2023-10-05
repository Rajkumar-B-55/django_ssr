from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from rest_framework import status
from rest_framework.response import Response

from product_svc.models import Product
from users.decorators import allowed_users
from .forms import OrderForm, OrderUpdateForm
from .models import Order


@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def order_update_status(request, uuid):
    try:
        order = Order.objects.get(order_uuid=uuid)
        if not order:
            return render(request, 'error_page.html', {'error_message': 'Order not found'}, status=404)

        if request.method == 'POST':
            form = OrderUpdateForm(request.POST, instance=order)
            if form.is_valid():
                order.status = form.cleaned_data['status']
                order.save()
                messages.success(request, f'{order.order_uuid} Order Status updated')
                return redirect('dashboard_order')
        else:
            form = OrderUpdateForm(instance=order)
            context = {'form': form}
            return render(request, 'orders/order_update.html', context)
    except Order.DoesNotExist:
        return render(request, 'error_page.html', {'error_message': 'Order not found'}, status=404)
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)})


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def delete(request, pk):
    try:
        order = Order.objects.filter(pk=pk).first()
        if not order:
            return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)},
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required(login_url='login')
def place_order(request):
    try:
        user = request.user
        if user is not None:
            form = OrderForm(request.POST)
            if form.is_valid():
                product_name = form.cleaned_data['product']
                product = Product.objects.get(name=product_name)
                order_quantity = form.cleaned_data['quantity']
                order_add = Order(user=user, status='Pending', product=product, quantity=order_quantity)
                order_add.save()
                messages.success(request, 'Order placed Successfully')
                return redirect('dashboard_order')
            else:
                messages.warning(request, 'Invalid form data. Please check the fields.')
                return redirect('dashboard_order')

    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)},
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@login_required(login_url='login')
@allowed_users(allowed_roles='admin')
def order_list(request):
    try:
        user = request.user
        user_order = Order.objects.filter(user_id=user.id)
        response_data = [
            {
                "order_tracking_id": str(order.order_uuid),
                "order_status": order.status,
                "product_name": order.product.name,
                "product_quantity": order.product.quantity,
                "product_price": float(order.product.price),
                "product_description": order.product.description,
                "product_total_price": float(order.get_total_item_price),
                "customer_name": order.user.first_name,
                "customer_email": order.user.email,
            }

            for order in user_order
        ]

        return Response(response_data, status=status.HTTP_200_OK)
    except Exception as e:
        return render(request, 'error_page.html', {'error_message': str(e)},
                      status=status.HTTP_500_INTERNAL_SERVER_ERROR)
