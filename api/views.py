from django.shortcuts import render
from rest_framework import generics
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormView
from django.contrib.auth import login,logout,authenticate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import AuthenticationForm
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .models import Pedidos,User,Productos
from .serializers import PedidosSerializer,UserSerializer, ProductosSerializer
from django.core.mail import send_mail
from django.conf import settings

#Creamos nuestra vista de clase PedidosList
class PedidosList(generics.ListCreateAPIView):
    queryset = Pedidos.objects.all()
    serializer_class = PedidosSerializer
    permission_classes = (IsAuthenticated,) #Comprueba que el usuario está logeado

#Creamos nuestra vista de clase ProductosList
class ProductosList(generics.ListCreateAPIView):
    queryset = Productos.objects.all()
    serializer_class = ProductosSerializer
    permission_classes = (IsAuthenticated,) #Comprueba que el usuario está logeado

#Creamos nuestra vista de clase UserList
class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    #permission_classes = (IsAuthenticated,)

#Creamos nuestra vista de clase Login
class Login(FormView):
    template_name = "api/login.html" 
    form_class = AuthenticationForm
    success_url = reverse_lazy('api:pedidos_list') #si todo es correcto, nos llevará a nuestra página de pedidos

    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self,request,*args,**kwargs): #Comprobamos si nuestro user se ha autentificado
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.get_success_url())
        else:
            return super(Login,self).dispatch(request,*args,*kwargs)

    def form_valid(self,form): #Validamos nuestro registro con su correspondiente token
        user = authenticate(username = form.cleaned_data['username'], password = form.cleaned_data['password'])
        token,_ = Token.objects.get_or_create(user = user)
        if token:
            login(self.request, form.get_user())
            return super(Login,self).form_valid(form)

#Creamos nuestra vista de Logout, eliminamos el token de autentificación y nos devuelve un HTTP_200_OK si es correcto
class Logout(APIView):
    def get(self,request, format = None):
        request.user.auth_token.delete()
        logout(request)
        return Response(status = status.HTTP_200_OK)

#Creamos nuestra vista de envio mail, y nos devuelve un HTTP_200_OK si es correcto
class Mailing(APIView):
    def get(self,request):
        asunto = 'Pedido generado correctamente'
        mensaje = str(Pedidos.objects.all())
        email_from = settings.EMAIL_HOST_USER
        email_to = ["email destino"]

        send_mail(
            asunto,
            mensaje,
            email_from,
            email_to,
            fail_silently=False,
        )
        return Response(status = status.HTTP_200_OK)