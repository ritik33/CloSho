from django.db import models
from users.models import User
from django.core.validators import MinValueValidator
import uuid


class Category(models.Model):
    name = models.CharField(max_length=50)
    img = models.ImageField(
        upload_to='cate_img', height_field=None, width_field=None, max_length=None)

    def __str__(self):
        return self.name


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, max_length=10,
                          primary_key=True, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50, null=True)
    description = models.CharField(max_length=250, null=True)
    price = models.DecimalField(
        validators=[MinValueValidator(1)], decimal_places=2, max_digits=5)
    image = models.ImageField(
        upload_to='prod_img', height_field=None, width_field=None, max_length=None)
    choose_sex = (
        ('All', 'All'),
        ('Male', 'Male'),
        ('Female', 'Female'),
    )
    sex = models.CharField(max_length=50, choices=choose_sex, null=True)
    digital = models.BooleanField(default=False)
    reviews = models.PositiveIntegerField(default=0)
    stock = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.name


class ShippingAddress(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254, default=User().email)
    address = models.CharField(max_length=254)
    city = models.CharField(max_length=50)
    choose_state = (
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chandigarh', 'Chandigarh'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ("Dadar and Nagar Haveli", "Dadar and Nagar Haveli"),
        ("Daman and Diu", "Daman and Diu"),
        ("Delhi", "Delhi"),
        ("Lakshadweep", "Lakshadweep"),
        ("Puducherry", "Puducherry"),
        ("Goa", "Goa"),
        ("Gujarat", "Gujarat"),
        ("Haryana", "Haryana"),
        ("Himachal Pradesh", "Himachal Pradesh"),
        ("Jammu and Kashmir", "Jammu and Kashmir"),
        ("Jharkhand", "Jharkhand"),
        ("Karnataka", "Karnataka"),
        ("Kerala", "Kerala"),
        ("Madhya Pradesh", "Madhya Pradesh"),
        ("Maharashtra", "Maharashtra"),
        ("Manipur", "Manipur"),
        ("Meghalaya", "Meghalaya"),
        ("Mizoram", "Mizoram"),
        ("Nagaland", "Nagaland"),
        ("Odisha", "Odisha"),
        ("Punjab", "Punjab"),
        ("Rajasthan", "Rajasthan"),
        ("Sikkim", "Sikkim"),
        ("Tamil Nadu", "Tamil Nadu"),
        ("Telangana", "Telangana"),
        ("Tripura", "Tripura"),
        ("Uttar Pradesh", "Uttar Pradesh"),
        ("Uttarakhand", "Uttarakhand"),
        ("West Bengal", "West Bengal"),
    )
    state = models.CharField(max_length=50, choices=choose_state)
    choose_country = (
        ('India', 'India'),
    )
    country = models.CharField(max_length=50, choices=choose_country)
    zipcode = models.PositiveIntegerField()
    phone_number = models.PositiveIntegerField()

    def __str__(self):
        return self.customer.username


class OrderItem(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField(default=1)
    ordered = models.BooleanField(default=False)

    @property
    def item_total_price(self):
        total = self.product.price * self.quantity
        return total

    def __str__(self):
        return self.product.name


class Order(models.Model):
    id = models.UUIDField(default=uuid.uuid4, max_length=10,
                          primary_key=True, unique=True)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    shipping_address = models.ForeignKey(
        ShippingAddress, on_delete=models.SET_NULL, null=True)
    products = models.ManyToManyField(OrderItem)
    created = models.DateTimeField(auto_now_add=True, null=True)
    cancel_reason = models.CharField(max_length=100, null=True)
    cancelled = models.BooleanField(default=False)
    completed = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=100, null=True)

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


class Review(models.Model):
    customer = models.ForeignKey(
        User, default=None, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=254)
    img = models.ImageField(
        upload_to='review_img', height_field=None, width_field=None, max_length=None)
    created = models.DateTimeField(auto_now_add=True)
