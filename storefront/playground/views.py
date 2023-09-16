from django.shortcuts import render
from store.models import *
from tags.models import *
from django.db import transaction

# Create your views here.


def say_hello(request):
    # Transaction return roll back if one query is faild
    with transaction.atomic():
        order = Order()
        order.customer_id = 1
        order.save()

        item = OrderItem()
        item.order = order
        item.product_id = 1
        # item.product_id = -1 Roll back
        item.quantity = 1
        item.unit_price = 10
        item.save()

    return render(
        request,
        "hello.html",
        {
            "name": "Anup",
        },
    )
