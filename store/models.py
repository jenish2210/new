from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    def __str__(self):
        return self.name

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    created_at = models.DateTimeField(auto_now_add=True)
    paid = models.BooleanField(default=False)
    address = models.TextField(blank=True)
    def total(self):
        return sum(item.subtotal() for item in self.items.all())
    def __str__(self):
        return f'Order #{self.id} by {self.user}'

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    def subtotal(self):
        return self.price * self.quantity
    def __str__(self):
        return f'{self.quantity} x {self.product}'
