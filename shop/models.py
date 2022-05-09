from itertools import product
from urllib import request
from django.db import models
from users.models import User
from django.core.validators import MinValueValidator
import uuid


class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, max_length=10, primary_key=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    price = models.DecimalField(
        validators=[MinValueValidator(1)], decimal_places=2, max_digits=5)
    image = models.ImageField(
        upload_to='prod_img', height_field=None, width_field=None, max_length=None)
    choose_sex = (
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    sex = models.CharField(max_length=50, choices=choose_sex)
    stock = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    phone_number = models.PositiveIntegerField()
    address = models.CharField(max_length=254)
    zipcode = models.PositiveIntegerField()
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    country = models.CharField(max_length=50)

    def __str__(self):
        return self.customer.username


class OrderItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    @property
    def item_total_price(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return self.product.name


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, max_length=10, primary_key=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(OrderItem)
    created = models.DateTimeField(auto_now_add=True, null=True)
    completed = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100)

    class Meta:
        ordering = ('-created',)

    @property
    def order_price(self):
        order_items = self.products.all()
        total_price = sum([item.item_total_price for item in order_items])
        return total_price

    @property
    def order_quantity(self):
        order_items = self.products.all()
        total_quantity = sum([item.quantity for item in order_items])
        return total_quantity

    def __str__(self):
        return str(self.id)


class Wishlist(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
