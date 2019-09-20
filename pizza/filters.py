from django_filters import FilterSet, CharFilter

from pizza.models import Order, Pizza


class OrderFilter(FilterSet):
    phone_number = CharFilter(lookup_expr='icontains')
    delivery_status = CharFilter(lookup_expr='iexact')
    first_name = CharFilter(lookup_expr='icontains')
    last_name = CharFilter(lookup_expr='icontains')
    address_line_1 = CharFilter(lookup_expr='icontains')
    address_line_2 = CharFilter(lookup_expr='icontains')
    postal_code = CharFilter(lookup_expr='icontains')
    city = CharFilter(lookup_expr='icontains')
    country = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Order
        fields = (
            'delivery_status', 'phone_number', 'first_name', 'last_name', 'address_line_1', 'address_line_2',
            'postal_code', 'city', 'country'
        )


class PizzaFilter(FilterSet):

    flavor = CharFilter(lookup_expr='icontains')
    size = CharFilter(lookup_expr='icontains')
    count = CharFilter(lookup_expr='icontains')
    order = CharFilter(lookup_expr='icontains')

    class Meta:
        model = Pizza
        fields = (
            'flavor', 'size', 'count' , 'order'
        )
