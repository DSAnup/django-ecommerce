from rest_framework_nested import routers
from . import views
from pprint import pprint

router = routers.DefaultRouter()
router.register("products", views.ProductViewSet, basename="products")
router.register("collections", views.CollectionViewSet)
router.register("carts", views.CartViewSet)

products_router = routers.NestedDefaultRouter(router, "products", lookup="product")
products_router.register(
    "reviews", views.ReviewViewSet, basename="products-review-details"
)

carts_router = routers.NestedDefaultRouter(router, "carts", lookup="cart")
carts_router.register("items", views.CartItemViewSet, basename="cart-item-details")

# URLConf
urlpatterns = router.urls + products_router.urls + carts_router.urls
