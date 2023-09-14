from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product, Order, OrderItem, Customer
from django.db.models import Min, Max, Avg, Count, Sum, Q, F, Value

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
    # Products: inventory = price
    queryset3 = Product.objects.filter(inventory=F("unit_price"))
    # secondary table
    queryset3 = Product.objects.filter(inventory=F("collection__id"))
    querysetSort = Product.objects.order_by("-title", "unit_price")
    # earliest
    earliestProduct = Product.objects.earliest("unit_price")
    # limit
    querysetLimit = Product.objects.all()[:5]
    querysetLimit = Product.objects.all()[5:15]
    # Select fields in query return dictionary
    querysetSelectFields = Product.objects.values("id", "title", "collection__title")
    # Select fields in query return tuple
    querysetSelectFields = Product.objects.values_list(
        "id", "title", "collection__title"
    )
    # Select products that have been ordered and sort them by title
    productOrder = (
        OrderItem.objects.values("id", "unit_price", "product__title")
        .distinct()
        .order_by("product__title")
    )
    productOrder = Product.objects.filter(
        id__in=OrderItem.objects.values("product_id").distinct()
    ).order_by("title")
    # select related inner join with collection table (1)
    select_related = Product.objects.select_related("collection").all()
    prefetch_related = Product.objects.prefetch_related("promotions").all()
    prefetch_related2 = (
        Product.objects.prefetch_related("promotions")
        .select_related("collection")
        .all()
    )

    # get the last 5 orders with their customer and products
    getlast5Orders = (
        Order.objects.select_related("customer")
        .prefetch_related("orderitem_set__product")
        .all()
        .order_by("-placed_at")[:5]
    )
    # create new field in template uses
    annonate_object = Customer.objects.annotate(is_new=Value(True), new_id=F("id") + 1)
    return render(
        request,
        "hello.html",
        {
            "name": "Anup",
            "products": list(select_related),
            "result": list(getlast5Orders),
            "result2": list(annonate_object),
        },
    )
