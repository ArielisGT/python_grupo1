# lógica de negocio de alquiler de coches

from .models import Vehicle, VehicleAvailable, VehicleRent
import datetime
from django.core.exceptions import ObjectDoesNotExist
from django.utils.dateparse import parse_datetime


# error durante alquiler
class RentError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(message)


# parsear intervalo de fechas
def parse_datetime_interval(begin, end):
    datetime_begin = parse_datetime(begin)
    datetime_end = parse_datetime(end)

    if datetime_begin > datetime_end:
        datetime_begin, datetime_end = datetime_end, datetime_begin

    return datetime_begin, datetime_end


# encontrar vehículos disponibles en un intervalo de tiempo
def find_available_vehicles(
        datetime_begin: datetime.datetime,
        datetime_end: datetime.datetime
):
    vehicle_availables = VehicleAvailable.availables.filter(
        time_begin__lte=datetime_begin,
        time_end__gte=datetime_end
    )

    # TODO optimizar
    vehicles = []
    for vehicle_available in vehicle_availables:
        vehicles.append(
            Vehicle.vehicles.get(id=vehicle_available.vehicle_id)
        )

    return vehicles


# alquilar un vehículo
def rent_vehicle(
        vehicle_id,
        client_id,
        rent_time_begin: datetime.datetime,
        rent_time_end: datetime.datetime,
        pay_account
):
    # comprobar que el vehículo está disponible

    try:
        rented_vehicle_available: VehicleAvailable = \
            VehicleAvailable.availables.get(
                vehicle_id=vehicle_id,
                time_begin__lte=rent_time_begin,
                time_end__gte=rent_time_end
            )
    except ObjectDoesNotExist:
        raise RentError('El vehículo no está disponible.')

    # crear alquiler

    VehicleRent.rents.create(
        vehicle_id=vehicle_id,
        client_id=client_id,
        time_begin=rent_time_begin,
        time_end=rent_time_end,
        pay_account=pay_account
    )

    # dividir intervalo de disponibilidad en dos,
    # con el intervalo de alquiler en medio

    rented_vehicle_available_time_end = rented_vehicle_available.time_end

    rented_vehicle_available.time_end = rent_time_begin

    rented_vehicle_available.save(update_fields=['time_end'])

    VehicleAvailable.availables.create(
        vehicle_id=vehicle_id,
        time_begin=rent_time_end,
        time_end=rented_vehicle_available_time_end
    )


# cancelar alquiler de un vehículo
def cancel_vehicle_rent(rent_id):
    # eliminar alquiler

    rent = VehicleRent.rents.get(id=rent_id)

    rent_vehicle_id = rent.vehicle_id
    rent_time_begin = rent.time_begin
    rent_time_end = rent.time_end

    rent.delete()

    # restaurar intervalo de disponibilidad

    available_before_rent = VehicleAvailable.availables.get(
        vehicle_id=rent_vehicle_id,
        time_end=rent_time_begin
    )

    available_after_rent = VehicleAvailable.availables.get(
        vehicle_id=rent_vehicle_id,
        time_begin=rent_time_end
    )

    available_before_rent.time_end = available_after_rent.time_end

    available_before_rent.save(update_fields=['time_end'])
    available_after_rent.delete()


# obtener alquileres de un cliente a partir de una fecha
def get_client_rents(client_id, time_from):
    return VehicleRent.rents.filter(
        client_id=client_id,
        time_end__gte=time_from
    )
