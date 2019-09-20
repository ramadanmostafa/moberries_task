from rest_framework import serializers

from pizza.models import Order, Pizza


class PizzaSerializer(serializers.ModelSerializer):

    class Meta:
        model = Pizza
        fields = ('id', 'flavor', 'size', 'count')

    def validate_count(self, value):
        if value < 1:
            raise serializers.ValidationError("count should be 1 at least")
        return value


class OrderSerializer(serializers.ModelSerializer):
    pizza = PizzaSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = (
            'id', 'delivery_status', 'pizza', 'first_name', 'last_name', 'address_line_1', 'address_line_2',
            'postal_code', 'city', 'country', 'phone_number'
        )
