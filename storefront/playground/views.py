from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import *
from tags.models import *
from django.contrib.contenttypes.models import ContentType

# Create your views here.


def say_hello(request):
    collection = Collection()
    collection.title = "Video Games"
    collection.featured_product = Product(pk=1)
    collection.save()
    print(collection.id)

    return render(
        request,
        "hello.html",
        {
            "name": "Anup",
        },
    )
