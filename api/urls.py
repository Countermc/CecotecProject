from django.urls import path
from .views import PedidosList,UserList,ProductosList

urlpatterns = [
    path('pedidos/',PedidosList.as_view(), name = 'pedidos_list'),
    path('productos/',ProductosList.as_view(), name = 'productos_list'),
    path('user/',UserList.as_view(), name = 'user_list'),
]