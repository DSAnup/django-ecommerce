from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from store.models import Product

# Create your views here.


def say_hello(request):
    query_set = Product.objects.all()
    print(query_set)
    # pk is set as primary key
    productExists = Product.objects.filter(pk=0).exists()
    # return None
    print(productExists)
    return render(request, "hello.html", {"name": "Anup"})
