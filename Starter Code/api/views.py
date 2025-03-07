from django.db.models import Max
from django.shortcuts import get_object_or_404, render
from . models import Product, Order, OrderItem
from .serializers import ProductSerializer, OrderSerializer, ProductInfoSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

# @api_view(['GET'])
# def product_list(request):
#     products = Product.objects.all()
#     print(type(products)) 
#     serializer = ProductSerializer(products, many=True)
#     return Response(serializer.data)

class ProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class StockProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all().filter(stock__gt = 0)
    serializer_class = ProductSerializer

class nonStockProductListAPIView(generics.ListAPIView):
    queryset = Product.objects.all().exclude(stock__gt = 0)
    serializer_class = ProductSerializer

# @api_view(['GET'])
# def product_detail(request, pk):
#     product = get_object_or_404(Product, pk=pk)
#     print(type(product))  
#     serializer = ProductSerializer(product)
#     return Response(serializer.data)

class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

# @api_view(['GET'])
# def order_list(request):
#     orders = Order.objects.prefetch_related(
#         'items',
#         'items__product',
#     ).all()
#     print(type(orders))  
#     serializer = OrderSerializer(orders, many=True)
#     return Response(serializer.data)

class OrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related(
        'items',
        'items__product',
    ).all()
    serializer_class = OrderSerializer

class UserOrderListAPIView(generics.ListAPIView):
    queryset = Order.objects.prefetch_related(
        'items__product',
    )
    serializer_class = OrderSerializer
    def get_queryset(self):
        return self.get_queryset().filter(user_id=self.request.user.id)

@api_view(['GET'])
def product_info(request):
    products = Product.objects.all()
    serializer = ProductInfoSerializer({
        'products' : products,
        'count': len(products),
        'max_price' : products.aggregate(max_price = Max('price'))['max_price']
    })
    return Response(serializer.data)
    