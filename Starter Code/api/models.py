from math import prod
import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)

    @property 
    def in_stock(self):
        return self.stock > 0
    def __str__(self):
        return self.name

class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'
    
    orderID = models.UUIDField(primary_key=True, editable=False, default = uuid.uuid4)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10, 
        choices = StatusChoices.choices,
        default=StatusChoices.PENDING
    )
    products = models.ManyToManyField(Product, through='OrderItem', related_name='orders')

    def __str__(self):
        return f'{self.orderID} by {self.user.username}'



class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name = 'items'
        )
    product = models.ForeignKey(
        Product, 
        on_delete=models.CASCADE,
        )
    quantity = models.PositiveIntegerField()

    @property
    def item_subtotal(self):
        return self.product.price * self.quantity
    
    def __str__(self):  
        return f'{self.quantity} x {self.product.name} in Order {self.order.orderID}'
