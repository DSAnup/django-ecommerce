from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import *
from tags.models import *
from django.contrib.contenttypes.models import ContentType

# Create your views here.


def say_hello(request):
    tags = TaggedItem.objects.get_tags_for(Product, 1)

    return render(
        request,
        "hello.html",
        {
            "name": "Anup",
            "tags": list(tags),
        },
    )
