from rest_framework import serializers
from .models import Pedidos,User,Productos
from django.contrib.auth.models import User
from django.core.mail import send_mail


class PedidosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pedidos
        fields = (
            'id',
            'producto',
            'cantidad',
        )
    
    def get(self,request):
        asunto = 'Pedido generado correctamente'
        mensaje = 'correito'
        email_from = settings.EMAIL_HOST_USER
        email_to = ["jmoreno@xsistemas.es"]

        send_mail(
            asunto,
            mensaje,
            email_from,
            email_to,
            fail_silently=False,
        )
        return Response(status = status.HTTP_200_OK)

class ProductosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Productos
        fields = (
            'id',
            'nombrepro',
            'colorpro',
            'tipopro',
            'stock',
        )

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def validate_username(self, data):        
        users = User.objects.filter(username = data)
        if len(users) !=0:
            raise serializers.ValidationError("El Usuario ya existe")
        else:
            return data


