from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),
    path('<uuid:pk>/', views.shopSingle, name='shop-single'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('add-to-cart/<uuid:pk>/<int:quantity>/',
         views.addToCart, name='add-to-cart'),
    path('reduce-from-cart/<uuid:pk>/',
         views.reduceFromCart, name='reduce-from-cart'),
    path('remove-from-cart/<uuid:pk>/',
         views.removeFromCart, name='remove-from-cart'),
    path('process-order/', views.processOrder, name='process-order'),
]
