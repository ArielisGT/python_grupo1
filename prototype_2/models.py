from django.db import models
from django.contrib.auth.models import User


# TODO eliminar client y admin

# admin
# class Admin(models.Model):
#     # nombre de usuario
#     username = models.CharField(max_length=20)
#
#     # contraseña
#     # TODO password cifrado
#     password = models.CharField(max_length=80)
#
#     # dirección email
#     email = models.CharField(max_length=80)

# cliente
# class Client(models.Model):
#     # nombre
#     name = models.CharField(max_length=160)
#
#     # dirección email
#     email = models.CharField(max_length=80)
#
#     # contraseña
#     # TODO password cifrado
#     password = models.CharField(max_length=80)
#
#     clients = models.Manager()


# cliente
class Client(models.Model):
    # usuario
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # dirección
    address = models.CharField(max_length=160)

    clients = models.Manager()


# vehículo
class Vehicle(models.Model):
    # marca y modelo
    model = models.CharField(max_length=40)

    # matrícula
    number = models.CharField(max_length=10)

    vehicles = models.Manager()


# intervalo vehículo disponible
class VehicleAvailable(models.Model):
    # vehículo disponible
    vehicle = models.ForeignKey(Vehicle, on_delete=models.RESTRICT)

    # intervalo de disponibilidad
    time_begin = models.DateTimeField()
    time_end = models.DateTimeField()

    availables = models.Manager()


# alquiler de vehículo
class VehicleRent(models.Model):
    # vehículo alquilado
    vehicle = models.ForeignKey(Vehicle, on_delete=models.RESTRICT)

    # cliente
    client = models.ForeignKey(Client, on_delete=models.RESTRICT)

    # intervalo de alquiler
    time_begin = models.DateTimeField()
    time_end = models.DateTimeField()

    # cuenta de pago
    # TODO pay account not null (?)
    pay_account = models.CharField(max_length=160, null=True, blank=True)

    rents = models.Manager()
