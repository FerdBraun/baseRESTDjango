from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Sword, Customer, Order
from .serializers import SwordSerializer, CustomerSerializer, OrderSerializer
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import pmdarima as pm
import numpy as np


class CreateSwordApiView(APIView):
    def post(self, request, name, completed, damage, cost, *args, **kwargs):
        '''
        Create the Todo with given todo data
        '''
        data = {
            'name': name,
            'completed': completed,
            'damage': damage,
            'cost': cost,
        }
        serializer = SwordSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SwordListApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    # 1. List all
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        todos = Sword.objects.all()
        serializer = SwordSerializer(todos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create


class SwordDetailApiView(APIView):
    # add permission to check if user is authenticated
    # permission_classes = [permissions.IsAuthenticated]

    def get_object(self, sword_id):
        '''
        Helper method to get the object with given todo_id, and user_id
        '''
        try:
            return Sword.objects.get(id=sword_id)
        except Sword.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, sword_id, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
        todo_instance = self.get_object(sword_id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = SwordSerializer(todo_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 4. Update
    def put(self, request, sword_id, *args, **kwargs):
        '''
        Updates the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(sword_id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        data = {
            'name': request.data.get('name'),
            'completed': request.data.get('completed'),
            'damage': request.data.get('damage'),
            'cost': request.data.get('cost'),
        }
        serializer = SwordSerializer(instance=todo_instance, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 5. Delete
    def delete(self, request, sword_id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        todo_instance = self.get_object(sword_id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )


class CustomersOverview(APIView):
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.all()
        serializer = CustomerSerializer(customers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomersByIdView(APIView):
    def getDeleteUser(self, id):
        try:
            return Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return None

    def delete(self, request, id, *args, **kwargs):
        '''
        Deletes the todo item with given todo_id if exists
        '''
        todo_instance = self.getDeleteUser(id)
        if not todo_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        todo_instance.delete()
        return Response(
            {"res": "Object deleted!"},
            status=status.HTTP_200_OK
        )

    def getUserByid(self, id):
        try:
            return Customer.objects.get(id=id)
        except Customer.DoesNotExist:
            return None

    def get(self, request, id, *args, **kwargs):
        customer = self.getUserByid(id)
        if not customer:
            return Response(
                {"res": "Object mail does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CustomerSerializer(customer, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomersByEmailView(APIView):
    def getUser(self, email):
        try:
            return Customer.objects.get(email=email)
        except Customer.DoesNotExist:
            return None

    def get(self, request, email, *args, **kwargs):
        customer = self.getUser(email)
        if not customer:
            return Response(
                {"res": "Object mail does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CustomerSerializer(customer, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CustomersView(APIView):
    def getUser(self, email, password):
        try:
            return Customer.objects.get(email=email, password=password)
        except Customer.DoesNotExist:
            return None

    def get(self, request, email, password, *args, **kwargs):
        customer = self.getUser(email, password)
        if not customer:
            return Response(
                {"res": "Object mail does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = CustomerSerializer(customer, many=False)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, email, password, *args, **kwargs):
        data = {
            'email': email,
            'password': password
        }
        serializer = CustomerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrdersGetView(APIView):
    def get_object(self, idCustomer):

        try:
            return Order.objects.filter(idCustomer=idCustomer)
        except Order.DoesNotExist:
            return None

    # 3. Retrieve
    def get(self, request, idCustomer, *args, **kwargs):
        '''
        Retrieves the Todo with given todo_id
        '''
        todo_instance = self.get_object(idCustomer)
        if not todo_instance:
            return Response(
                {"res": "No Orders Found"},
                status=status.HTTP_200_OK
            )

        serializer = OrderSerializer(todo_instance, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderCreateView(APIView):
    def post(self, request, idCustomer, total, orderContains, count, *args, **kwargs):
        data = {
            'idCustomer': idCustomer,
            'orderContains': orderContains,
            'total': total,
            'count': count
        }
        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class MakePredictionsView(APIView):
    def get(self, request, *args, **kwargs):
        '''
        List all the todo items for given requested user
        '''
        Orders = Order.objects.all()
        serializer = OrderSerializer(Orders, many=True)
        stats_data = serializer.data

        df = pd.DataFrame(stats_data, columns=['count'])
        df.index = pd.date_range(start='1/1/2020', periods=len(stats_data))
        train, test = df[:int(len(df) * 0.7)], df[int(len(df) * 0.7):]

        # Обучаем модель ARIMA
        model = ARIMA(train, order=(1, 0, 0))
        model_fit = model.fit()
        # Прогнозируем продажи на следующие 30 дней
        forecast = model_fit.forecast(steps=30)
        data_count = forecast.sum()
        print(data_count)
        #################################################
        df2 = pd.DataFrame(stats_data, columns=['total'])

        df2.index = pd.date_range(start='1/1/2020', periods=len(stats_data))
        print(df2)
        # Определение оптимальных параметров
        # best_fit = pm.auto_arima(df['count'], seasonal=False, suppress_warnings=True,
        #                        error_action='ignore')

        df2['total'] = df2['total'].astype(float)
        best_fit = pm.auto_arima(df2['total'], seasonal=False, suppress_warnings=True,
                                 error_action='ignore')
        # Печать оптимальных параметров
        print('Best model order: ', best_fit.order)
        train, test = df2[:int(len(df2) * 0.8)], df2[int(len(df2) * 0.8):]
        # Обучаем модель ARIMA
        model = ARIMA(train, order=(0, 0, 0))
        model_fit = model.fit()
        # Прогнозируем продажи на следующие 30 дней
        forecast = model_fit.forecast(steps=30)
        data_total = forecast.sum()
        print(forecast)
        print(data_total)
        print(df2['total'].sum())
        return Response([df['count'].sum(),df2['total'].sum(),int(data_count), int(data_total)], status=status.HTTP_200_OK)
