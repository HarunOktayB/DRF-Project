from django.db.models import Max
from django.shortcuts import get_object_or_404, render
from . models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    print(type(products)) 
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    print(type(product))  
    serializer = ProductSerializer(product)
    return Response(serializer.data)

@api_view(['GET'])
def order_list(request):
    orders = Order.objects.prefetch_related(
        'items',
        'items__product',
    ).all()
    print(type(orders))  
    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products' : products,
        'count': len(products),
        'max_price' : products.aggregate(max_price = Max('price'))['max_price']
    })

    return Response(serializer.data)
    