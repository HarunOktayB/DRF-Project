from dataclasses import fields
from itertools import product
from math import prod
from rest_framework import serializers
from api.models import User, Product, Order, OrderItem

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email'
        )


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            'name',
            'description',
            'price',
            'stock',
        )
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError('Price must be greater than 0')
        return value
    
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError('Stock must be greater than 0')
        return value
    
class OrderItemSerializer(serializers.ModelSerializer):
    # product = ProductSerializer()
    # YA SADECE NAME ve PRICE İSTESEYDİK?
    product_name = serializers.CharField(source = 'product.name')
    product_price = serializers.DecimalField(
        max_digits=10,
        decimal_places=2,
        source = 'product.price'
    )

    class Meta:
        model = OrderItem
        fields = (
            # 'order', Burada bunun olmasının hiç bir  anlamı yok zaten nested olarak order'ın içinde var, ve her orderItemin bir order'ı olmalı
            'product_name',
            'product_price',
            'quantity',
            'item_subtotal', # We can refer to properties ass well !
        )

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many = True, read_only = True)

    total_price = serializers.SerializerMethodField(method_name='my_total_price')

    def my_total_price(self, obj):
        return sum([item.item_subtotal for item in obj.items.all()])
        #item_subtotal da bizim oluşturduğumuz bir property olduğu için burada çağırabiliyoruz"
        # Normalde get_ ön takısı getirildiğinde default olarak çalışır ama biz burada method_name ile değiştirdik

    class Meta:
        model = Order
        fields = (
            'orderID',
            'user',
            'created_at',
            'status',
            'items',
            'total_price',
        )