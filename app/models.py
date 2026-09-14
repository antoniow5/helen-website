from django.db import models
from django.contrib.auth.models import User


class Product(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False)
    articul = models.CharField(max_length=50, null=False, blank=False, unique=True)
    variant_by_color = models.BooleanField(default=False)
    variant_by_size = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def create_variant_if_no_variation(self):
        if not self.variant_by_color and not self.variant_by_size:
            ProductVariant.objects.create(product=self, stock_quantity=0)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.create_variant_if_no_variation()   
    


class Color(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    hex_code = models.CharField(max_length=7, null=False, blank=False) 

    def save(self, *args, **kwargs):
        if not len(self.hex_code) == 7 or not self.hex_code.startswith('#'):
            raise ValueError("Hex code must be in the format '#RRGGBB'")
        super().save(*args, **kwargs)


    def __str__(self):
        return self.name



class Size(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    code = models.CharField(max_length=10, null=False, blank=False) 

    def __str__(self):
        return f"{self.name} - {self.code}"


class ProductVariant(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null = True, blank = True)
    size = models.ForeignKey(Size, on_delete=models.CASCADE, null = True, blank = True)
    stock_quantity = models.PositiveIntegerField(default=0)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['product', 'color', 'size'], name='unique_product_variant')
        ]


    def save(self, *args, **kwargs):
        if self.product.variant_by_color and not self.color:
            raise ValueError("Color must be specified for this product.")
        if self.product.variant_by_size and not self.size:
            raise ValueError("Size must be specified for this product.")
        super().save(*args, **kwargs)
        

    def __str__(self):
        if self.color:
            color = self.color.name
        else:
            color = '-'

        if self.size:
            size = self.size.name
        else:
            size = '-'
        return f"{self.product.name} - {color} - {size}"


class Cart(models.Model):
    session_id = models.CharField(max_length=100, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)



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


class Order(models.Model):    
    # cart = models.OneToOneField(Cart, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, default='Pending')  # e.g., Pending, Shipped, Delivered


    def __str__(self):
        return f"Order {self.id} - {self.status}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} x {self.product_variant.product.name} ({self.product_variant.color.name}, {self.product_variant.size.name})"
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='favorited_by')

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'product'], name='unique_favorite')
        ]

    def __str__(self):
        return f"{self.user.username} - {self.product.name}"