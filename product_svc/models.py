from django.db import models


class Product(models.Model):
    PRICE_UNITS_CHOICES = (('', 'Choose Product Unit'),
                           ('kg', 'kg'),
                           ('l', 'litre'),
                           ('pcs', 'pcs'),
                           ('gm', 'gm'),
                           ('m2', 'm2'),
                           ('m3', 'm3'),
                           ('ml', 'ml'),)
    name = models.CharField(max_length=50, null=True)
    price = models.DecimalField(max_digits=20, decimal_places=2)
    quantity = models.IntegerField(blank=False, default=1)
    unit = models.CharField(max_length=50, choices=PRICE_UNITS_CHOICES, default='')
    description = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'tbl_products'


