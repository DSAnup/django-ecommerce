from django.core.mail import send_mail, mail_admins, BadHeaderError, EmailMessage
from django.shortcuts import render
from store.models import *
from tags.models import *
from django.db import transaction

# Create your views here.


def sendmail(request):
    try:
        # send_mail("success", "hello world", "info@anup.com", ["bob@anup.com"])
        # mail_admins("subject", "message", html_message="message")
        message = EmailMessage(
            "subject", "message", "from@moshbuy.com", ["john@wick.com"]
        )
        message.attach_file("playground\static\images\kitchen.jpg")
        message.send()
    except BadHeaderError:
        pass
    return render(
        request,
        "hello.html",
        {
            "name": "Anup",
        },
    )


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
