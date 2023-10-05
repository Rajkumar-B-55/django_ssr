from django import forms

from order_svc.models import Order
from product_svc.models import Product


class OrderForm(forms.Form):
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        empty_label='Select a product',
        label='Select Product',
        required=True,
    )
    quantity = forms.IntegerField(
        label='Quantity',
        min_value=1,
        required=True,
    )
    status = forms.CharField(required=False)


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status']

