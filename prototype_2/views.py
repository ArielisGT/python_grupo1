from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.urls import reverse
from .models import Vehicle, Client, VehicleRent, VehicleAvailable
from . import logic_client, logic_rent
import datetime


def home_redirect(request):
    return HttpResponseRedirect("/pr2/client/login/form")

# admin: lista de vehículos
@login_required
def admin_vehicle_list(request):
    # acceso denegado
    # TODO página error 403
    if not request.user.is_staff:
        return redirect('client_rent_list')

    context = {
        'vehicles': Vehicle.vehicles.all()
    }
    return render(request, 'admin_vehicle_list.html', context)


# admin: ver datos de vehículo
@login_required
def admin_view_vehicle(request, vehicle_id):
    # acceso denegado
    # TODO página error 403
    if not request.user.is_staff:
        return redirect('client_rent_list')

    vehicle = Vehicle.vehicles.get(id=vehicle_id)

    context = {
        'vehicle': vehicle
    }
    return render(request, 'admin_vehicle_view.html', context)


# admin: formulario para crear vehículo
@login_required
def admin_create_vehicle_form(request):
    # acceso denegado
    # TODO página error 403
    if not request.user.is_staff:
        return redirect('client_rent_list')

    context = {
        'heading': 'New vehicle',
        'submitLabel': 'Add vehicle'
    }
    return render(request, 'admin_vehicle_form.html', context)


# admin: formulario para editar vehículo
@login_required
def admin_edit_vehicle_form(request, vehicle_id):
    # acceso denegado
    # TODO página error 403
    if not request.user.is_staff:
        return redirect('client_rent_list')

    vehicle = Vehicle.vehicles.get(id=vehicle_id)

    context = {
        'heading': f'Edit vehicle #{vehicle_id}',
        'vehicle': vehicle,
        'submitLabel': 'Save vehicle'
    }

    return render(request, 'admin_vehicle_form.html', context)


# admin: guardar vehículo
@login_required
def admin_save_vehicle(request):
    # acceso denegado
    # TODO página error 403
    if not request.user.is_staff:
        return redirect('client_rent_list')

    vehicle_id = request.POST.get('id')

    # es un vehículo nuevo?
    is_new_vehicle = not vehicle_id

    vehicle_model = request.POST.get('model')
    vehicle_number = request.POST.get('number')

    if is_new_vehicle:
        # insertar nuevo vehículo en BD
        vehicle = Vehicle.vehicles.create(
            model=vehicle_model,
            number=vehicle_number
        )

        # crear intervalo de disponibilidad
        begin_available = timezone.now()

        end_available = (
                datetime.datetime.max
                - datetime.timedelta(days=1)
        )

        VehicleAvailable.availables.create(
            vehicle_id=vehicle.id,
            time_begin=begin_available,
            time_end=end_available
        )

    else:
        # actualizar vehículo en BD
        vehicle = Vehicle.vehicles.get(id=vehicle_id)

        vehicle.model = vehicle_model
        vehicle.number = vehicle_number

        vehicle.save()

    return redirect('admin_vehicle_list')


# admin: eliminar vehículo
@login_required
def admin_delete_vehicle(request, vehicle_id):
    # acceso denegado
    # TODO página error 403
    if not request.user.is_staff:
        return redirect('client_rent_list')

    VehicleRent.rents.filter(vehicle_id=vehicle_id).delete()

    VehicleAvailable.availables.filter(vehicle_id=vehicle_id).delete()

    Vehicle.vehicles.get(id=vehicle_id).delete()

    return redirect('admin_vehicle_list')


# cliente
# form de login
def client_login_form(request):
    context = {}

    error = request.GET.get('error')
    if error == logic_client.ERROR_NO_USER:
        context['message'] = '''
        <div class="message">
            <p class="white">You have entered an invalid username &/or password</p>
        </div>
        '''

    return render(request, 'client_login_form_2.html', context)


# cliente
# login
def client_login(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = authenticate(request, username=username, password=password)

    if user is None:
        return HttpResponseRedirect(
            reverse('client_login_form_2')
            + f'?error={logic_client.ERROR_NO_USER}'
        )

    login(request, user)

    if request.user.is_staff:
        # el usuario es un admin
        return redirect('home')

    else:
        # el usuario es un cliente
        client = Client.clients.get(user_id=user.id)

        request.session['client_id'] = client.id

        return redirect('home')


# generación de datos temporales de valores de form de usuario
class UserFormValues:
    @staticmethod
    def get_values(request):
        return {
            'username': UserFormValues.get_form_value(request, 'username'),
            'email': UserFormValues.get_form_value(request, 'email'),
            'address': UserFormValues.get_form_value(request, 'address'),
            'password': UserFormValues.get_form_value(request, 'password'),
            'password2': UserFormValues.get_form_value(request, 'password2')
        }

    @staticmethod
    def get_form_value(request, key):
        value = request.POST.get(key)
        return value if value else ''


# cliente: formulario de registro
def client_signup_form(request):
    context = request.session['user_form_values']

    del request.session['user_form_values']

    error = request.GET.get('error')

    if error == logic_client.ERROR_NO_USERNAME:
        context['message'] = '''
         <div class="message">
            <p class="gray">Debe introducir un nombre de usuario.</p>
         </div>
        '''

    elif error == logic_client.ERROR_NO_PASSWORD:
        context['message'] = f'''
        <div class="message">
            <p class="gray">Debe introducir una contraseña de al menos {logic_client.PASSWORD_MIN_LENGTH} caracteres.</p>
        </div>
        '''

    elif error == logic_client.ERROR_PASSWORD_MISMATCH:
        context['message'] = '''
    <p class="gray">Las contraseñas que ha introducido no coinciden.</p>
    '''

    elif error == logic_client.ERROR_NO_EMAIL:
        context['message'] = '''
    <p class="gray">Debe introducir una dirección email válida.</p>
    '''

    elif error == logic_client.ERROR_NO_ADDRESS:
        context['message'] = '''
    <p class="gray">Debe introducir una dirección.</p>
    '''

    return render(request, 'client_signup_form.html', context)


# cliente: registrar
def client_signup(request):
    error = logic_client.signup(request)

    if error:
        request.session['user_form_values'] = UserFormValues.get_values(request)

        return HttpResponseRedirect(
            reverse('client_signup_form')
            + f'?error={error}'
        )

    return redirect('client_login_form_2')


# cliente: home
@login_required
def home(request):
    context = {}
    return render(request, 'home.html', context)


# alquiler: solicitar alquiler
# indicar intervalo de alquiler
@login_required
def rent_request_form(request):
    context = {}
    return render(request, 'rent_request_form.html', context)


# alquiler: seleccionar vehículo
@login_required
def rent_select_vehicle(request):
    rent_begin = request.GET.get("begin")
    rent_end = request.GET.get("end")

    if not rent_begin or not rent_end:
        return redirect('rent_request_form')

    rent_begin, rent_end = logic_rent.parse_datetime_interval(rent_begin, rent_end)

    vehicles = logic_rent.find_available_vehicles(rent_begin, rent_end)

    context = {
        'vehicles': vehicles,
        'rent_begin': rent_begin,
        'rent_end': rent_end
    }

    return render(request, 'rent_select_vehicle.html', context)


# alquiler: reservar vehículo seleccionado
# introducir datos de pago
@login_required
def rent_reserve_vehicle_form(request, vehicle_id, rent_begin, rent_end):
    vehicle = Vehicle.vehicles.get(id=vehicle_id)
    context = {
        'vehicle_id': vehicle_id,
        'rent_begin': rent_begin,
        'rent_end': rent_end,
        'vehicle': vehicle
    }
    return render(request, 'rent_reserve_vehicle.html', context)


# alquiler: confirmar alquiler
@login_required
def rent_confirm(request, vehicle_id, rent_begin, rent_end):
    if request.user.is_staff:
        # el usuario es un admin, no un cliente
        return redirect('admin_vehicle_list')

    rent_begin, rent_end = logic_rent.parse_datetime_interval(rent_begin, rent_end)

    pay_account = request.POST.get('payAccount')

    client_id = request.session['client_id']

    logic_rent.rent_vehicle(
        vehicle_id=vehicle_id,
        client_id=client_id,
        rent_time_begin=rent_begin,
        rent_time_end=rent_end,
        pay_account=pay_account
    )

    return redirect('client_rent_list')


# cliente: lista de alquileres del cliente
@login_required
def client_rent_list(request):
    if request.user.is_staff:
        # el usuario es un admin, no un cliente
        return redirect('admin_vehicle_list')

    client_id = request.session['client_id']

    time_from = datetime.datetime.now()

    rents = logic_rent.get_client_rents(
        client_id=client_id,
        time_from=time_from
    )

    context = {
        'rents': rents
    }

    return render(request, 'client_rent_list.html', context)


# alquiler: ver ficha de alquiler
@login_required
def rent_view(request, rent_id):
    rent = VehicleRent.rents.get(id=rent_id)

    context = {
        'rent': rent
    }

    return render(request, 'rent_view.html', context)


# alquiler: cancelar
@login_required
def rent_cancel(request, rent_id):
    logic_rent.cancel_vehicle_rent(rent_id)

    return redirect('client_rent_list')


# logout
@login_required
def logout_user(request):
    logout(request)
    return redirect('client_login_form_2')
