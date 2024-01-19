from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from secret_api.models import Sword, Customer, Order
from secret_api.views import CreateSwordApiView, SwordListApiView, SwordDetailApiView, CustomersOverview, \
    CustomersByIdView, \
    CustomersByEmailView, CustomersView, OrdersGetView, OrderCreateView


class SwordTests(APITestCase):
    def setUp(self):
        self.sword = Sword.objects.create(name="Test Sword", cost=10.0, damage=100, completed="Yes", sharpness=8.5)

    def test_create_sword(self):
        url = reverse('CreateSwordApiView',
                      kwargs={
                          'name': 'Excalibur',
                          'completed': 'true',
                          'damage': 100,
                          'cost': 1000
                      })
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Sword.objects.count(), 2)
        self.assertEqual(Sword.objects.get(id=2).name, 'Excalibur')

    def test_list_swords(self):
        url = reverse('SwordListApiView')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], 'Test Sword')

    def test_update_sword(self):
        url = reverse('SwordDetailApiView', args=[self.sword.id])
        data = {'name': 'Updated Sword', 'completed': 'No', 'damage': 200, 'cost': 20.0}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_sword = Sword.objects.get(id=self.sword.id)
        self.assertEqual(updated_sword.name, 'Updated Sword')

    def test_delete_sword(self):
        url = reverse('SwordDetailApiView', args=[self.sword.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Sword.objects.count(), 0)



class CustomerTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(email="test@example.com", password="1234")

    def test_get_customer_by_id(self):
        url = reverse('CustomersByIdView', args=[self.customer.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_delete_customer_by_id(self):
        url = reverse('CustomersByIdView', args=[self.customer.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Customer.objects.count(), 0)

    def test_get_customer_by_email(self):
        url = reverse('CustomersByEmailView', args=["test@example.com"])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_get_customer_by_email_and_password(self):
        url = reverse('CustomersView', kwargs={'email': "test@example.com", 'password': "1234"})
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_create_customer(self):
        url = reverse('CustomersView', kwargs={'email': "new@example.com", 'password': "5678"})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Customer.objects.count(), 2)
        self.assertEqual(Customer.objects.get(id=2).email, 'new@example.com')

    def test_list_customers(self):
        url = reverse('CustomersOverview')
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['email'], 'test@example.com')


class OrderTests(APITestCase):
    def setUp(self):
        self.customer = Customer.objects.create(email="test@example.com", password="1234")
        self.order = Order.objects.create(idCustomer=self.customer.id, total=100, orderContains="Item1")

    def test_create_order(self):
        url = reverse('OrderCreateView',
                      kwargs={'idCustomer': self.customer.id, 'orderContains': 'Item2', 'total': 200})
        response = self.client.post(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Order.objects.count(), 2)
        self.assertEqual(Order.objects.get(id=2).orderContains, 'Item2')

    def test_list_orders(self):
        url = reverse('OrdersGetView', args=[self.customer.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['orderContains'], 'Item1')
