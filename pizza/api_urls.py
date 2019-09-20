from pizza.api_views import OrderViewSet, PizzaViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'order/(?P<order_id>\d+)/pizza', PizzaViewSet, basename='pizza')
router.register(r'order', OrderViewSet, basename='order')
urlpatterns = router.urls
