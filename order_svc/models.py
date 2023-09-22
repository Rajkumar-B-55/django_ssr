import uuid

from django.contrib.auth import get_user_model
from django.db import models

from product_svc.models import Product

User = get_user_model()


class Order(models.Model):
    status = (
        ('Pending', 'Pending'),
        ('Delivered', 'Delivered'),
        ('Out for delivery', 'out for delivery')
    )
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(max_length=50, null=True, auto_now=True)
    status = models.CharField(max_length=100, null=True, choices=status)
    quantity = models.IntegerField(default=1, blank=False)
    order_uuid = models.UUIDField(editable=False, default=uuid.uuid4())

    class Meta:
        db_table = 'tbl_orders'

    @property
    def get_total_item_price(self):
        return self.quantity * self.product.price
