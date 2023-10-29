from django.core.validators import MinValueValidator
from django.db import models
from uuid import uuid4
from django.conf import settings
from django.contrib import admin

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2, validators=[MinValueValidator(1)]
    )  # defined the max digits & decimal digits
    slug = models.SlugField()
    inventory = models.IntegerField(validators=[MinValueValidator(1)])
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        "Collection", on_delete=models.PROTECT, related_name="products"
    )  # do not others production
    promotions = models.ManyToManyField("Promotion", blank=True)

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["title"]


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="store/images")


class Customer(models.Model):
    MemberShipBronze = "B"
    MemberShipSilver = "S"
    MemberShipGold = "G"
    MemberShipChoices = [
        (MemberShipBronze, "Bronze"),
        (MemberShipSilver, "Silver"),
        (MemberShipGold, "Gold"),
    ]
    phone = models.CharField(max_length=100)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MemberShipChoices, default=MemberShipBronze
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    @admin.display(ordering="user__first_name")
    def first_name(self):
        return self.user.first_name

    @admin.display(ordering="user__last_name")
    def last_name(self):
        return self.user.last_name

    class Meta:
        ordering = ["user__first_name", "user__last_name"]
        permissions = [("view_history", "Can view history")]


class Order(models.Model):
    PaymentStatusPending = "P"
    PaymentStatusComplete = "C"
    PaymentStatusFailed = "F"
    PaymentStatusChoices = [
        (PaymentStatusPending, "Pending"),
        (PaymentStatusComplete, "Complete"),
        (PaymentStatusFailed, "Failed"),
    ]

    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(
        max_length=1, choices=PaymentStatusChoices, default=PaymentStatusPending
    )

    class Meta:
        permissions = [("cancel_order", "Can cancel order")]


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=50, null=True)


class Collection(models.Model):
    title = models.CharField(max_length=255)
    featured_product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="+"
    )

    def __str__(self) -> str:
        return self.title

    class Meta:
        ordering = ["title"]


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, related_name="items")
    product = models.ForeignKey(
        Product, on_delete=models.PROTECT, related_name="orderitems"
    )
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = [["cart", "product"]]


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()


class Review(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="reviews"
    )
    name = models.CharField(max_length=255)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
