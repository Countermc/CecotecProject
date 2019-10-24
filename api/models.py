from django.db import models
from django.contrib.auth.models import User


class Productos(models.Model):
    id = models.AutoField(primary_key=True)
    nombrepro = models.CharField('Nombre', max_length=200)
    tipopro = models.CharField('Tipo', max_length=200)
    colorpro = models.CharField('Color', max_length=100)
    stock = models.IntegerField('Stock') 

    def __str__(self):
        return '{0},{1},{2}'.format(self.nombrepro, self.colorpro, self.tipopro)


class Pedidos(models.Model):
    id = models.AutoField(primary_key=True)
    producto = models.ManyToManyField(Productos)
    cantidad = models.IntegerField('Cantidad')
    

