from django.db import models
from django.contrib.auth.models import User


class BaseWeapon(models.Model):
    name = models.CharField(max_length=180, unique=True)
    cost = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    damage = models.IntegerField()
    completed = models.CharField(max_length=180)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Sword(BaseWeapon):
    sharpness = models.DecimalField(max_digits=2, decimal_places=1, default=0)


class Gun(BaseWeapon):
    range = models.DecimalField(max_digits=3, decimal_places=1, default=0)


class Customer(models.Model):
    email = models.CharField(unique=True, max_length=20)
    password = models.CharField(max_length=10, default='1234')

    def __str__(self):
        return self.email


class Order(models.Model):
    orderContains = models.CharField(max_length=200)
    idCustomer = models.IntegerField()
    total = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    orderDate = models.DateTimeField(auto_now_add=True)
    count = models.IntegerField(default=0)

    def __str__(self):
        return self.orderContains
