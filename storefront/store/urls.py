from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path("products/", views.ProductList.as_view()),
    path("products/<int:id>", views.ProductDetials.as_view()),
    path("collections/", views.collections_list),
    path("collections/<int:pk>", views.collections_details, name="collection-detail"),
]
