from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import *
from tags.models import *
from django.contrib.contenttypes.models import ContentType

# Create your views here.


def say_hello(request):
    Collection.objects.filter(pk=11).delete()

    return render(
        request,
        "hello.html",
        {
            "name": "Anup",
        },
    )
