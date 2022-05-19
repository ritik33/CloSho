from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from .models import Order, OrderItem, Product,  Wishlist, Category
from .forms import ShippingAddressForm, QuantityForm
from closho import settings
from django.contrib import messages
import razorpay


def shop(request):
    search = request.GET.get('search')
    category = request.GET.get('category')
    sex = request.GET.get('sex')
    priceSort = request.GET.get('sort')
    products = Product.objects.all()
    categories = Category.objects.all()
    if search:
        products = products.filter(name__icontains=search)
    if category:
        products = products.filter(category__name=category)
    if sex:
        products = products.filter(sex=sex)
    if priceSort:
        products = products.order_by(priceSort)
    context = {'categories': categories, 'products': products}
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
def addToCart(request, pk, quantity=1):
    product = get_object_or_404(Product, id=pk)
    if product.stock < quantity:
        messages.warning(
            request, 'Your selected quantity exceeded available stock.')
        return redirect('shop')
    order_item, created = OrderItem.objects.get_or_create(
        product=product, customer=request.user, ordered=False, defaults={'quantity': quantity})  # defaults doesn't work in get() call
    order_qs = Order.objects.filter(
        customer=request.user, completed=False)
    if order_qs.exists():
        order = order_qs[0]  # filter returns a queryset that's why taking [0]
        if order.products.filter(product__id=pk).exists():
            order_item.quantity += quantity
            order_item.save(update_fields=['quantity'])
            product.stock -= quantity
            product.save(update_fields=['stock'])
            messages.success(request, 'Product quantity is updated.')
            return redirect('cart')
        else:
            order.products.add(order_item)
            product.stock -= quantity
            product.save(update_fields=['stock'])
            messages.success(request, 'Product is added to your cart.')
            return redirect('cart')
    else:
        order = Order.objects.create(customer=request.user)
        order.products.add(order_item)
        product.stock -= quantity
        product.save(update_fields=['stock'])
        messages.success(request, 'Product is added to your cart.')
        return redirect('cart')


@login_required
def reduceFromCart(request, pk):
    product = get_object_or_404(Product, id=pk)
    order_qs = Order.objects.filter(
        customer=request.user, completed=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__id=pk).exists():
            order_item = OrderItem.objects.filter(
                product=product, customer=request.user, ordered=False)[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save(update_fields=['quantity'])
                product.stock += 1
                product.save(update_fields=['stock'])
                messages.success(request, 'Product quantity is updated.')
            else:
                order.products.remove(order_item)
                order_item.delete()
                product.stock += 1
                product.save(update_fields=['stock'])
                messages.warning(request, 'Product removed from your cart.')
            return redirect('cart')
        else:
            messages.warning(request, 'Product is not in your cart.')
            return redirect('cart')
    else:
        messages.warning(request, 'You do not have an active order.')
        return redirect('cart')


@login_required
def removeFromCart(request, pk):
    product = get_object_or_404(Product, id=pk)
    order_qs = Order.objects.filter(
        customer=request.user, completed=False)
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__id=pk).exists():
            order_item = OrderItem.objects.filter(
                product=product, customer=request.user, ordered=False)[0]
            product.stock += order_item.quantity
            product.save(update_fields=['stock'])
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


@login_required
def wishlist(request):
    products = Wishlist.objects.all()
    context = {'products': products}
    return render(request, 'wishlist.html', context)


@login_required
def addRemoveWishlist(request, pk):
    product = get_object_or_404(Product, id=pk)
    wishlist, created = Wishlist.objects.get_or_create(
        customer=request.user, product=product)
    if not created:
        wishlist.delete()
        messages.info(request, 'Product removed from wishlist.')
        return redirect('shop')
    else:
        messages.info(request, 'Product wishlisted.')
        return redirect('shop')


@login_required
def checkout(request):
    customer = request.user
    products = OrderItem.objects.filter(
        customer=customer, ordered=False)
    if not products:
        messages.info(request, 'Cart is empty.')
        return redirect('shop')
    order, created = Order.objects.get_or_create(
        customer=customer, completed=False)
    if request.method == 'POST':
        form = ShippingAddressForm(data=request.POST)
        if form.is_valid():
            shipping_address = form.save(commit=False)
            shipping_address.customer = request.user
            shipping_address.save()
            order.shipping_address = shipping_address
            order.save()
            return redirect('payment')
        else:
            messages.warning(request, 'Invalid data.')
            return redirect('checkout')
    else:
        form = ShippingAddressForm
        context = {'products': products, 'order': order, 'form': form}
        return render(request, 'checkout.html', context)


@login_required
def payment(request):
    try:
        order = Order.objects.get(customer=request.user, completed=False)
    except Order.DoesNotExist:
        messages.info(request, 'Cart is empty.')
        return redirect('shop')
    if not order.order_quantity:
        messages.info(request, 'Cart is empty.')
        return redirect('shop')
    client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    DATA = {
        "amount": int(order.order_price * 100),
        "currency": "INR",
    }
    razorpay_order = client.order.create(data=DATA)
    callback_url = "/callback/"
    razorpay_id = razorpay_order['id']
    order.razorpay_order_id = razorpay_order['id']
    order.save(update_fields=['razorpay_order_id'])
    context = {'order': order, 'callback_url': callback_url,
               'razorpay_id': razorpay_id, 'razorpay_key_id': settings.RAZOR_KEY_ID}
    return render(request, 'payment.html', context)


@require_http_methods(["POST"])
@csrf_exempt
def callback(request):
    for key, value in request.POST.items():
        if key == "razorpay_order_id":
            razorpay_order_id = value
        elif key == "razorpay_payment_id":
            razorpay_payment_id = value
        elif key == "razorpay_signature":
            razorpay_signature = value

    client = razorpay.Client(
        auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
    verify = client.utility.verify_payment_signature({
        'razorpay_order_id': razorpay_order_id,
        'razorpay_payment_id': razorpay_payment_id,
        'razorpay_signature': razorpay_signature
    })
    if verify:
        customer = request.user
        OrderItem.objects.filter(
            customer=customer, ordered=False).update(ordered=True)
        order = Order.objects.get(customer=customer, completed=False)
        order.completed = True
        order.razorpay_payment_id = razorpay_payment_id
        order.razorpay_signature = razorpay_signature
        order.save(update_fields=['completed',
                   'razorpay_payment_id', 'razorpay_signature'])

        return redirect('payment-success')
    return redirect('payment-failure')
