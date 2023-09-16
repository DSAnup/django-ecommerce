from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import *
from tags.models import *
from django.db.models import (
    Min,
    Max,
    Avg,
    Count,
    Sum,
    Q,
    F,
    Value,
    Func,
    ExpressionWrapper,
    DecimalField,
)
from django.db.models.functions import Concat
from django.contrib.contenttypes.models import ContentType

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
    annonate_object_concat = Customer.objects.annotate(
        # CONCAT
        full_name=Func(F("first_name"), Value(" "), F("last_name"), function="CONCAT")
    )
    annonate_object_concat = Customer.objects.annotate(
        # CONCAT
        full_name=Concat("first_name", Value(" "), "last_name")
    )
    annonate_object_group_by = Customer.objects.annotate(
        # CONCAT
        order_count=Count("order")
    )
    discounted_price = ExpressionWrapper(
        F("unit_price") * 0.8, output_field=DecimalField()
    )
    annonate_object_expressionwrapper = Product.objects.annotate(
        discounted_price=discounted_price
    )
    # LIKE Operations
    customer_with_com_count = Customer.objects.filter(
        email__icontains=".com"
    ).aggregate(count=Count("id"))
    customer_with_com = Customer.objects.filter(email__icontains=".com")

    # collection that don't have featured product
    collection_dont_featuredproduct = Collection.objects.filter(
        featured_product__isnull=True
    )
    # Products: inventory < 10
    lowInventory = Product.objects.filter(inventory__lt=10)
    # Order placed by customer with id = 1
    OrderPlacedByCustomer1 = Order.objects.filter(customer__id=1)
    # Order items for products in collection 3
    OrderItemCollection3 = OrderItem.objects.filter(product__collection__id=3)

    content_type = ContentType.objects.get_for_model(Product)

    tags = TaggedItem.objects.select_related("tag").filter(
        content_type=content_type, object_id=1
    )

    return render(
        request,
        "hello.html",
        {
            "name": "Anup",
            "products": list(select_related),
            "result": list(getlast5Orders),
            "result2": list(OrderItemCollection3),
            "tags": list(tags),
        },
    )
