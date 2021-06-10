# lógica de negocio de alquiler de clientes

from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import Client

# errores
ERROR_NO_USER = 'no_user'
ERROR_NO_USERNAME = 'no_username'
ERROR_NO_PASSWORD = 'no_password'
ERROR_PASSWORD_MISMATCH = 'password_mismatch'
ERROR_NO_EMAIL = 'no_email'
ERROR_NO_ADDRESS = 'no_address'

# longitud mínima de contraseña
PASSWORD_MIN_LENGTH = 10


# registrar usuario
def signup(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    password2 = request.POST.get('password2')
    email = request.POST.get('email')
    address = request.POST.get('address')

    if not username:
        return ERROR_NO_USERNAME

    if not password or len(password) < PASSWORD_MIN_LENGTH:
        return ERROR_NO_PASSWORD

    if password != password2:
        return ERROR_PASSWORD_MISMATCH

    try:
        if not email:
            raise ValidationError('no email')
        validate_email(email)
    except ValidationError:
        return ERROR_NO_EMAIL

    if not address:
        return ERROR_NO_ADDRESS

    user = User.objects.create_user(username, email, password)

    Client.clients.create(
        user=user,
        address=address
    )

    # no hay error
    return None
