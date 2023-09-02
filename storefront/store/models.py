from django.db import models

# Create your models here.


class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    unit_price = models.DecimalField(
        max_digits=6, decimal_places=2
    )  # defined the max digits & decimal digits
    slug = models.SlugField()
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    collection = models.ForeignKey(
        "Collection", on_delete=models.PROTECT
    )  # do not others production
    promotions = models.ManyToManyField("Promotion")


class Customer(models.Model):
    MemberShipBronze = "B"
    MemberShipSilver = "S"
    MemberShipGold = "G"
    MemberShipChoices = [
        (MemberShipBronze, "Bronze"),
        (MemberShipSilver, "Silver"),
        (MemberShipGold, "Gold"),
    ]
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=100)
    birth_date = models.DateField(null=True)
    membership = models.CharField(
        max_length=1, choices=MemberShipChoices, default=MemberShipBronze
    )


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


class Address(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)


class Collection(models.Model):
    title = models.CharField(max_length=255)
    feature_product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, related_name="+"
    )


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()


class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField()
