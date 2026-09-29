from django.db import models
from django.contrib.auth.models import User
from .product import ProductVariant


class Cart(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, unique=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['cart', 'product_variant'], name='unique_cart_item')
        ]


    def __str__(self):
        return f"{self.quantity} x {self.product_variant.product.name} ({self.product_variant.color.name}, {self.product_variant.size.name})"
