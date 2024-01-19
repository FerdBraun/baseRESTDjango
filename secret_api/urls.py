from django.urls import path, include
from .views import (
    SwordListApiView,
    SwordDetailApiView,
    CustomersView,
    CustomersOverview,
    CustomersByIdView,
    CreateSwordApiView,
    CustomersByEmailView,
    OrdersGetView, OrderCreateView, MakePredictionsView
)

urlpatterns = [
    path('api/swords', SwordListApiView.as_view(), name='SwordListApiView'),
    path('api/sword/<int:sword_id>', SwordDetailApiView.as_view(), name='SwordDetailApiView'),
    path('api/sword/<str:name>,<str:completed>,<int:damage>,<int:cost>', CreateSwordApiView.as_view(), name='CreateSwordApiView'),
    path('api/customer/<str:email>,<str:password>', CustomersView.as_view(), name='CustomersView'),
    path('api/customer/<str:email>', CustomersByEmailView.as_view(), name='CustomersByEmailView'),
    path('api/customerByid/<int:id>', CustomersByIdView.as_view(), name='CustomersByIdView'),
    path('api/customers', CustomersOverview.as_view(), name='CustomersOverview'),
    path('api/order/<int:idCustomer>,<str:orderContains>,<int:total>,<int:count>', OrderCreateView.as_view(), name='OrderCreateView'),
    path('api/getorder/<int:idCustomer>', OrdersGetView.as_view(), name='OrdersGetView'),
    path('api/makepred', MakePredictionsView.as_view(), name='MakePredictionsView'),

]
