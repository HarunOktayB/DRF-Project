from django.urls import path
from . import views

urlpatterns = [
    # path('products/', views.product_list, name='product-list'),
    path('products/', views.ProductListAPIView.as_view(), name='product-list'),
    path('products/stock', views.StockProductListAPIView.as_view(), name='stock-products'),
    path('products/out-of-stock', views.nonStockProductListAPIView.as_view(), name='out-of-stock-products'),
    path('orders/', views.OrderListAPIView.as_view(), name='order-list'),
    
    path('products/info/', views.product_info, name='product-info'),    
    path('products/<int:pk>/', views.ProductDetailAPIView.as_view(), name='product-detail'),
]
