from django.shortcuts import get_object_or_404, render
from . models import Product
from .serializers import ProductSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def product_list(request):
    products = Product.objects.all()
    print(type(products))  # ✅ Ekledik: Tipini kontrol edelim
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)

@api_view(['GET'])
def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    print(type(product))  # ✅ Ekledik: Tipini kontrol edelim
    serializer = ProductSerializer(product)
    return Response(serializer.data)