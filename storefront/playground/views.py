from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import *
from tags.models import *
from django.contrib.contenttypes.models import ContentType

# Create your views here.


def say_hello(request):
    # collection = Collection(pk=11)
    # collection.title = "Games"
    # collection.featured_product = None
    # collection.save()
    # print(collection.id)
    Collection.objects.filter(pk=11).update(title="Games two")

    return render(
        request,
        "hello.html",
        {
            "name": "Anup",
        },
    )
