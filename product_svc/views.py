from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from users.auth import IsAdminUser
from .forms import ProductForm
from .models import Product


class ProductGetAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk=None, *args, **kwargs):
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
            return Response(data={'error': str(e.args[1])}, status=status.HTTP_404_NOT_FOUND)


class ProductAddAPI(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, *args, **kwargs):
        try:
            form = ProductForm(data=request.data)
            if form.is_valid():
                form.save()
                return Response(data={'Success': form.data}, status=status.HTTP_201_CREATED)
            return Response(form.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response(data={'error': str(e.args[1])}, status=status.HTTP_404_NOT_FOUND)


class ProductPutAPI(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, pk, *args, **kwargs):
        try:
            if pk is None:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            product = Product.objects.filter(pk=pk).first()
            if not product:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            if 'name' in request.data:
                product.name = request.data['name']
            if 'price' in request.data:
                product.price = request.data['price']
            if 'quantity' in request.data:
                product.quantity = request.data['quantity']
            if 'unit' in request.data:
                product.unit = request.data['unit']
            if 'description' in request.data:
                product.description = request.data['description']

                # Save the updated product
            product.save()

            return Response({'message': 'Product updated successfully'})
        except Exception as e:
            return Response(data={'error': str(e.args[1])}, status=status.HTTP_404_NOT_FOUND)


class ProductDeleteAPI(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, pk, *args, **kwargs):
        try:
            product = Product.objects.filter(pk=pk).first()
            if not product:
                return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)
            product.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            return Response(data={'error': str(e.args[1])}, status=status.HTTP_404_NOT_FOUND)
