from rest_framework import serializers
from .models import Sword, Customer, Order, Gun


class BaseSerializer(serializers.ModelSerializer):
    pass


class SwordSerializer(BaseSerializer):
    class Meta:
        model = Sword
        fields = ["id", "name", "damage", "completed", 'cost','sharpness']
class GunSerializer(BaseSerializer):
    class Meta:
        model = Gun
        fields = ["id", "name", "damage", "completed", 'cost','range']

class CustomerSerializer(BaseSerializer):
    class Meta:
        model = Customer
        fields = ["id", "email", "password"]


class OrderSerializer(BaseSerializer):
    class Meta:
        model = Order
        fields = ["orderContains", "idCustomer", "orderDate", 'total','count']
