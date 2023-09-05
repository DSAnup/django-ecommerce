from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Order, OrderItem
from django.db.models import Min, Max, Avg, Count, Sum, Q

# Create your views here.


def say_hello(request):
    queryset = Product.objects.filter(collection__title="Beauty").filter(
        title__icontains="coffee"
    )
    orderCount = Order.objects.aggregate(count=Count("id"))
    product1Sold = OrderItem.objects.filter(product__id=1).aggregate(
        units_sold=Sum("quantity")
    )
    customer1Order = Order.objects.filter(customer__id=1).aggregate(count=Count("id"))
    minPriceCollection3 = Product.objects.filter(collection__id=3).aggregate(
        min_value=Min("unit_price"),
        max_value=Max("unit_price"),
        avg_value=Avg("unit_price"),
    )
    # Products: inventory < 10 AND price < 20
    queryset1 = Product.objects.filter(inventory__lt=10, unit_price__lt=20)

    # Products: inventory < 10 OR price < 20
    queryset2 = Product.objects.filter(Q(inventory__lt=10) | Q(unit_price__lt=20))
    # Products: inventory < 10 and not less than price < 20
    queryset2 = Product.objects.filter(Q(inventory__lt=10) & ~Q(unit_price__lt=20))
    return render(
        request,
        "hello.html",
        {
            "name": "Anup",
            "products": list(queryset),
            "products1": list(queryset1),
            "products2": list(queryset2),
            "totalOrder": orderCount,
            "product1Sold": product1Sold,
            "customer1Order": customer1Order,
            "minPriceCollection3": minPriceCollection3,
        },
    )
