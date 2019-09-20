from enum import Enum

from django.db import models

class Timestampable(models.Model):
    updated_at = models.DateTimeField('date updated', auto_now=True)
    created_at = models.DateTimeField('date created', auto_now_add=True)

    class Meta:
        abstract = True


class Order(Timestampable):

    class DeliveryStatus(Enum):
        not_started = 'not_started'
        out_for_delivery = 'out_for_delivery'
        delivered = 'delivered'

    delivery_status = models.CharField(
        max_length=50, null=False, choices=[(tag.name, tag.value,) for tag in DeliveryStatus],
        default=DeliveryStatus.not_started.value
    )

    # this data about the user should be in different model. i did it like this just for simplicity
    first_name = models.CharField('first name', max_length=30, blank=False)
    last_name = models.CharField('last name', max_length=150, blank=False)
    address_line_1 = models.CharField(blank=True, max_length=250)
    address_line_2 = models.CharField(blank=True, max_length=250)
    postal_code = models.CharField(blank=True, max_length=5)
    city = models.CharField(blank=True, max_length=250)
    country = models.CharField(blank=True, max_length=250)
    phone_number = models.CharField(null=False, max_length=25)

    def is_delivered(self):
        return self.delivery_status == Order.DeliveryStatus.delivered.value


class Pizza(Timestampable):
    class Flavors(Enum):
        salami = 'salami'
        cheese = 'cheese'
        margarita = 'margarita'
        vegan = 'vegan'
        vegetables = 'vegetables'
        macaroni = 'macaroni'

    class Size(Enum):
        small = 'small'
        medium = 'medium'
        large = 'large'

    flavor = models.CharField(
        max_length=50, null=False, choices=[(tag.name, tag.value,) for tag in Flavors]
    )

    size = models.CharField(
        max_length=50, null=False, choices=[(tag.name, tag.value,) for tag in Size]
    )
    count = models.PositiveIntegerField(default=0)
    order = models.ForeignKey(Order, null=False, on_delete=models.CASCADE, related_name='pizza')
