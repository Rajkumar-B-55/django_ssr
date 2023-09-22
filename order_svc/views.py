from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from product_svc.models import Product
from .forms import OrderForm
from .models import Order


class OrderAddAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        try:
            product_id = request.query_params.get('product_id')
            user = request.user
            product = Product.objects.filter(id=product_id).first()

            if product is None:
                return Response(data={'error': 'Product Not available'}, status=status.HTTP_404_NOT_FOUND)

            if user is not None:
                form = OrderForm(request.POST)
                if form.is_valid():
                    order_status = form.cleaned_data['status']
                    order_quantity = form.cleaned_data['quantity']

                    # Create a new order associated with the user and product
                    order_add = Order(user=user, product=product, status=order_status, quantity=order_quantity)
                    order_add.save()

                    return Response(
                        data={'msg': f"Order placed Successfully. Order Track id is {order_add.order_uuid}"})
                else:
                    return Response(data={"msg": "Invalid form data. Please check your input."},
                                    status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'User Not authenticated'}, status=status.HTTP_401_UNAUTHORIZED)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class OrderGetAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
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
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

#
#
# def put(self, request, pk):
#     try:
#         order = Order.objects.filter(pk=pk).first()
#         if not order:
#             return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
#
#         form = OrderForm(instance=order, data=request.data)
#         if form.is_valid():
#             form.save()
#             return Response({'message': 'Order updated successfully'})
#         return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
#
#
# def delete(self, request, pk):
#     try:
#         order = Order.objects.filter(pk=pk).first()
#         if not order:
#             return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)
#         order.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#     except Exception as e:
#         return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
