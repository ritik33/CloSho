from django.urls import path
from . import views
from django.views.generic import TemplateView


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
    path('wishlist/', views.wishlist, name='wishlist'),
    path('add-remove-wishlist/<uuid:pk>', views.addRemoveWishlist,
         name='add-remove-wishlist'),
    path('payment/', views.payment, name='payment'),
    path('callback/', views.callback, name='callback'),
    path('payment-success/', TemplateView.as_view(template_name='payment-success.html'),
         name='payment-success'),
    path('payment-failure/', TemplateView.as_view(template_name='payment-failure.html'),
         name='payment-failure'),
]
