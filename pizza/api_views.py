from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import ValidationError

from pizza.filters import OrderFilter, PizzaFilter
from pizza.models import Order, Pizza
from pizza.serializers import OrderSerializer, PizzaSerializer


class OrderViewSet(viewsets.ModelViewSet):
    """
    create, update, list, delete or get details of an order
    """
    filter_class = OrderFilter
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    filter_backends = (DjangoFilterBackend,)

    def perform_update(self, serializer):
        if Order.objects.get(pk=self.kwargs['pk']).is_delivered():
            raise ValidationError("Cannot update a delivered order")
        super().perform_update(serializer)


class PizzaViewSet(viewsets.ModelViewSet):
    """
    create, update, list, delete or get details of a pizza related to an already created order
    """
    filter_class = PizzaFilter
    serializer_class = PizzaSerializer
    filter_backends = (DjangoFilterBackend,)

    def get_queryset(self):
        return Pizza.objects.filter(order_id=self.kwargs['order_id'])

    def perform_create(self, serializer):
        Pizza.objects.create(order_id=self.kwargs['order_id'], **serializer.validated_data)

    def perform_update(self, serializer):
        if Order.objects.get(pk=self.kwargs['order_id']).is_delivered():
            raise ValidationError("Cannot update a delivered order")
        super().perform_update(serializer)
