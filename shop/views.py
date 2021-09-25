import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from .models import Order, OrderItem, Product, ShippingAddress
from .forms import ShippingAddressForm, QuantityForm
from django.http import JsonResponse
from django.contrib import messages
import datetime


def shop(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'shop.html', context)


def shopSingle(request, pk):
    product = Product.objects.get(id=pk)
    if request.method == 'POST':
        form = QuantityForm(request.POST)
        if form.is_valid():
            quantity = form.cleaned_data.get('quantity')
            addToCart(request, pk, quantity)
            return redirect('cart')
    else:
        form = QuantityForm
    context = {'product': product, 'form': form}
    return render(request, 'shop-single.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(
            customer=customer, completed=False)
        products = OrderItem.objects.filter(
            customer=customer, ordered=False)
    else:
        order = {'order_price': 0, 'order_quantity': 0}
        products = []
    context = {'products': products, 'order': order}
    return render(request, 'cart.html', context)


@login_required
def checkout(request):
    customer = request.user
    order, created = Order.objects.get_or_create(
        customer=customer, completed=False)
    products = OrderItem.objects.filter(
        customer=customer, ordered=False)
    if request.method == 'POST':
        form = ShippingAddressForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = email = form.cleaned_data.get('email')
            phone_number = form.cleaned_data.get('phone_number')
            address = form.cleaned_data.get('address')
            zipcode = form.cleaned_data.get('zipcode')
            city = form.cleaned_data.get('city')
            state = form.cleaned_data.get('state')
            country = form.cleaned_data.get('country')
            shipping_address = ShippingAddress(
                customer=customer,
                name=name,
                email=email,
                phone_number=phone_number,
                address=address,
                zipcode=zipcode,
                city=city,
                state=state,
                country=country
            )
            shipping_address.save()
            order.shipping_address = shipping_address
            order.save()
            return render(request, 'payment.html', {'order': order})

    else:
        form = ShippingAddressForm
    context = {'products': products, 'order': order, 'form': form}
    return render(request, 'checkout.html', context)


def processOrder(request):
    order = Order.objects.get(customer=request.user, completed=False)
    transaction_id = datetime.datetime.now().timestamp()
    order.transaction_id = transaction_id
    order.completed = True
    order.save()
    return JsonResponse('Payment Submitted', safe=False)


def addToCart(request, pk, quantity=1):
    product = get_object_or_404(Product, id=pk)
    order_item, created = OrderItem.objects.get_or_create(
        product=product, customer=request.user, ordered=False, defaults={'quantity': quantity})
    order_qs = Order.objects.filter(
        customer=request.user, completed=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__id=pk).exists():
            order_item.quantity += quantity
            order_item.save()
            messages.success(request, 'Product quantity is updated.')
            return redirect('cart')
        else:
            order.products.add(order_item)
            messages.success(request, 'Product is added to your cart.')
            return redirect('cart')
    else:
        order = Order.objects.create(customer=request.user)
        order.products.add(order_item)
        messages.success(request, 'Product is added to your cart.')
        return redirect('cart')


def reduceFromCart(request, pk):
    product = get_object_or_404(Product, id=pk)
    order_qs = Order.objects.filter(
        customer=request.user, completed=False)  # filter returns a queryset
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__id=pk).exists():
            order_item = OrderItem.objects.filter(
                product=product, customer=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
                messages.success(request, 'Product quantity is updated.')
            else:
                order.products.remove(order_item)
                order_item.delete()
                messages.warning(request, 'Product removed from your cart.')
            return redirect('cart')
        else:
            messages.warning(request, 'Product is not in your cart.')
            return redirect('cart')
    else:
        messages.warning(request, 'You do not have an active order.')
        return redirect('cart')


def removeFromCart(request, pk):
    product = get_object_or_404(Product, id=pk)
    order_qs = Order.objects.filter(
        customer=request.user, completed=False)  # filter returns a queryset
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__id=pk).exists():
            order_item = OrderItem.objects.filter(
                product=product, customer=request.user, ordered=False)[0]
            order.products.remove(order_item)
            order_item.delete()
            messages.warning(request, 'Product removed from your cart.')
            return redirect('cart')
        else:
            messages.warning(request, 'Product is not in your cart.')
            return redirect('cart')
    else:
        messages.warning(request, 'You do not have an active order.')
        return redirect('cart')
