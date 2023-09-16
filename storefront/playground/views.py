from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import *
from tags.models import *
from django.contrib.contenttypes.models import ContentType

# Create your views here.


def say_hello(request):
    content_type = ContentType.objects.get_for_model(Product)
    tags = TaggedItem.objects.select_related("tag").filter(
        content_type=content_type, object_id=1
    )

    return render(
        request,
        "hello.html",
        {
            "name": "Anup",
            "tags": list(tags),
        },
    )
