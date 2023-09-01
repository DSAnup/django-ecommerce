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
    PlacedAt = models.DateTimeField(auto_now_add=True)
    PaymentStatus = models.CharField(
        max_length=1, choices=PaymentStatusChoices, default=PaymentStatusPending
    )


class Address(models.Model):
    Customer = models.OneToOneField(
        Customer, on_delete=models.CASCADE, primary_key=True
    )
    Street = models.CharField(max_length=255)
    City = models.CharField(max_length=255)
