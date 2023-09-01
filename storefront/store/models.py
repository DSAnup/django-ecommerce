from django.db import models

# Create your models here.


class Product(models.Model):
    Title = models.CharField(max_length=255)
    Description = models.TextField()
    Price = models.DecimalField(
        max_digits=6, decimal_places=2
    )  # defined the max digits & decimal digits
    Inventory = models.IntegerField()
    LastUpdate = models.DateTimeField(auto_now=True)
    Collection = models.ForeignKey(
        "Collection", on_delete=models.PROTECT
    )  # do not others production
    Promotions = models.ManyToManyField("Promotion")


class Customer(models.Model):
    MemberShipBronze = "B"
    MemberShipSilver = "S"
    MemberShipGold = "G"
    MemberShipChoices = [
        (MemberShipBronze, "Bronze"),
        (MemberShipSilver, "Silver"),
        (MemberShipGold, "Gold"),
    ]
    FirstName = models.CharField(max_length=100)
    LastName = models.CharField(max_length=100)
    Email = models.EmailField(unique=True)
    Phone = models.CharField(max_length=100)
    BirthDate = models.DateField(null=True)
    MemberShip = models.CharField(
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

    Customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    PlacedAt = models.DateTimeField(auto_now_add=True)
    PaymentStatus = models.CharField(
        max_length=1, choices=PaymentStatusChoices, default=PaymentStatusPending
    )


class Address(models.Model):
    Customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    Street = models.CharField(max_length=255)
    City = models.CharField(max_length=255)


class Collection(models.Model):
    Title = models.CharField(max_length=255)


class OrderItem(models.Model):
    Order = models.ForeignKey(Order, on_delete=models.PROTECT)
    Product = models.ForeignKey(Product, on_delete=models.PROTECT)
    Quantity = models.PositiveSmallIntegerField()
    UnitPrice = models.DecimalField(max_digits=6, decimal_places=2)


class Cart(models.Model):
    CreatedAt = models.DateTimeField(auto_now_add=True)


class CartItem(models.Model):
    Cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    Quantity = models.PositiveSmallIntegerField()


class Promotion(models.Model):
    Description = models.CharField(max_length=255)
    Discount = models.FloatField()
