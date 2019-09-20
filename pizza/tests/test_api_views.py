from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from pizza.models import Order, Pizza


class TestOrderViewSet(APITestCase):

    def setUp(self) -> None:
        self.maxDiff = None
        self.url = reverse('order-list')

    def _create_pizza_order(self):
        order = Order.objects.create(
            country='de',
            first_name='first_name',
            last_name='last_name',
            phone_number='phone'
        )
        pizza = Pizza.objects.create(
            flavor=Pizza.Flavors.cheese.name,
            size=Pizza.Size.medium.name,
            count=3,
            order=order
        )
        return order, pizza

    def __assert_valid_response(self, data, pizza_count, expected_order_data, expected_pizza_data={}):
        self.assertIn('delivery_status', data)
        self.assertIn('pizza', data)
        self.assertIn('first_name', data)
        self.assertIn('last_name', data)
        self.assertIn('address_line_1', data)
        self.assertIn('address_line_2', data)
        self.assertIn('postal_code', data)
        self.assertIn('phone_number', data)
        self.assertIn('country', data)
        self.assertIn('city', data)
        self.assertIn('id', data)
        self.assertEqual(pizza_count, len(data['pizza']))
        for k, v in expected_order_data.items():
            self.assertEqual(data[k], v)
        for pizza_dict in data['pizza']:
            self.assertIn('flavor', pizza_dict)
            self.assertIn('size', pizza_dict)
            self.assertIn('count', pizza_dict)
            self.assertIn('id', pizza_dict)
            for k, v in expected_pizza_data.items():
                self.assertEqual(pizza_dict[k], v)

    def test_list_api_empty(self):
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.json())

    def test_list_api_with_orders(self):
        for _ in range(5):
            self._create_pizza_order()
        response = self.client.get(self.url)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response_json = response.json()
        self.assertEqual(5, len(response_json))

    def test_list_api_with_orders_filter_delivery_status1(self):
        for _ in range(5):
            self._create_pizza_order()
        response = self.client.get(self.url, data={'delivery_status': Order.DeliveryStatus.delivered.name})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response_json = response.json()
        self.assertEqual([], response_json)

    def test_list_api_with_orders_filter_delivery_status2(self):
        for _ in range(5):
            self._create_pizza_order()
        last_order = Order.objects.last()
        last_order.delivery_status = Order.DeliveryStatus.delivered.value
        last_order.save()
        response = self.client.get(self.url, data={'delivery_status': Order.DeliveryStatus.delivered.name})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response_json = response.json()
        self.assertEqual(1, len(response_json))

    def test_list_api_with_orders_filter_customer1(self):
        for _ in range(5):
            self._create_pizza_order()
        response = self.client.get(self.url, data={'phone_number': 'test'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response_json = response.json()
        self.assertEqual([], response_json)

    def test_list_api_with_orders_filter_customer2(self):
        for _ in range(5):
            self._create_pizza_order()
        last_order = Order.objects.last()
        last_order.phone_number = 'test123'
        last_order.save()
        response = self.client.get(self.url, data={'phone_number': 'test'})
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        response_json = response.json()
        self.assertEqual(1, len(response_json))

    def test_create_api_empty_order(self):
        data = {}
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                'first_name': ['This field is required.'], 'last_name': ['This field is required.'],
                'phone_number': ['This field is required.']
            },
            response.json()
        )

    def test_create_api_valid(self):
        data = {
            'first_name': 'ramadan', 'last_name': 'khalifa', 'address_line_1': '5',
            'address_line_2': '1', 'postal_code': '2', 'city': '3', 'country': '4', 'phone_number': '+49017617789557'
        }
        response = self.client.post(self.url, data=data, format='json')
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual(1, Order.objects.all().count())
        self.__assert_valid_response(
            response.json(), 0,
            expected_order_data={
                'delivery_status': 'not_started', 'first_name': 'ramadan', 'last_name': 'khalifa',
                'address_line_1': '5', 'address_line_2': '1', 'postal_code': '2', 'city': '3', 'country': '4',
                'phone_number': '+49017617789557'
            },
            expected_pizza_data={
                'flavor': 'cheese', 'size': 'large', 'count': 1
            }
        )

    def test_update_api_valid(self):
        order, pizza = self._create_pizza_order()
        data = {
            'delivery_status': 'delivered', 'first_name': 'test', 'last_name': 'test', 'address_line_1': 'test',
            'address_line_2': 'test', 'postal_code': 'test', 'city': 'test', 'country': 'test', 'phone_number': 'test',
        }

        url = reverse('order-detail', args=(order.pk, ))
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)

        self.__assert_valid_response(
            response.json(), 1,
            expected_order_data={
                'delivery_status': 'delivered', 'first_name': 'test', 'last_name': 'test', 'address_line_1': 'test',
                'address_line_2': 'test', 'postal_code': 'test', 'city': 'test', 'country': 'test',
                'phone_number': 'test',
            },
        )

    def test_update_api_delivered_order(self):
        order, pizza = self._create_pizza_order()
        order.delivery_status = Order.DeliveryStatus.delivered.value
        order.save()
        data = {
            'delivery_status': Order.DeliveryStatus.not_started.value, 'first_name': 'test', 'last_name': 'test',
            'address_line_1': 'test', 'address_line_2': 'test', 'postal_code': 'test', 'city': 'test',
            'country': 'test', 'phone_number': 'test',
        }

        url = reverse('order-detail', args=(order.pk, ))
        response = self.client.put(url, data=data, format='json')
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(['Cannot update a delivered order'], response.json())

    def test_delete_api_valid(self):
        order, _ = self._create_pizza_order()
        url = reverse('order-detail', args=(order.pk, ))
        response = self.client.delete(url, format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, Order.objects.all().count())
        self.assertEqual(0, Pizza.objects.all().count())


class TestPizzaViewSet(APITestCase):

    def setUp(self) -> None:
        self.order = Order.objects.create(
            country='de',
            first_name='first_name',
            last_name='last_name',
            phone_number='phone'
        )
        self.pizza = Pizza.objects.create(
            flavor=Pizza.Flavors.cheese.name,
            size=Pizza.Size.medium.name,
            count=3,
            order=self.order
        )
        self.url = reverse('pizza-list', args=(self.order.pk, ))
        self.url_details = reverse('pizza-detail', args=(self.order.pk, self.pizza.pk))

    def test_with_wrong_order_id(self):
        url = reverse('pizza-list', args=('78787878', ))
        response = self.client.get(url, format='json')

        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([], response.json())

    def test_list(self):
        response = self.client.get(self.url, format='json')
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual([{'id': self.pizza.pk, 'flavor': 'cheese', 'size': 'medium', 'count': 3}], response.json())

    def test_create_valid(self):
        data = {'flavor': 'cheese', 'size': 'large', 'count': 1}
        response = self.client.post(self.url, format='json', data=data)
        self.assertEqual(status.HTTP_201_CREATED, response.status_code)
        self.assertEqual({'flavor': 'cheese', 'size': 'large', 'count': 1}, response.json())
        self.assertEqual(1, Pizza.objects.filter(**{'flavor': 'cheese', 'size': 'large', 'count': 1}).count())

    def test_create_invalid(self):
        response = self.client.post(self.url, format='json', data={})
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual({'flavor': ['This field is required.'], 'size': ['This field is required.']}, response.json())

    def test_update_valid(self):
        data = {'flavor': 'salami', 'size': 'small', 'count': 12}
        response = self.client.put(self.url_details, format='json', data=data)
        self.assertEqual(status.HTTP_200_OK, response.status_code)
        self.assertEqual({'flavor': 'salami', 'size': 'small', 'count': 12, 'id': self.pizza.id}, response.json())
        self.assertEqual(1, Pizza.objects.filter(**{'flavor': 'salami', 'size': 'small', 'count': 12}).count())

    def test_update_delivered_order(self):
        self.order.delivery_status = Order.DeliveryStatus.delivered.value
        self.order.save()
        data = {'flavor': 'salami', 'size': 'small', 'count': 12}
        response = self.client.put(self.url_details, format='json', data=data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(['Cannot update a delivered order'], response.json())

    def test_update_invalid(self):
        data = {'flavor': 'salamii', 'size': 'smalll', 'count': -3}
        response = self.client.put(self.url_details, format='json', data=data)
        self.assertEqual(status.HTTP_400_BAD_REQUEST, response.status_code)
        self.assertEqual(
            {
                'flavor': ['"salamii" is not a valid choice.'], 'size': ['"smalll" is not a valid choice.'],
                'count': ['Ensure this value is greater than or equal to 0.']
            },
            response.json()
        )

    def test_delete(self):
        response = self.client.delete(self.url_details, format='json')
        self.assertEqual(status.HTTP_204_NO_CONTENT, response.status_code)
        self.assertEqual(0, Pizza.objects.all().count())
