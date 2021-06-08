from django.urls import path
from . import views

urlpatterns = [
    # admin
    path(
        'admin/vehicle/list/',
        views.admin_vehicle_list,
        name='admin_vehicle_list'
    ),
    path(
        'admin/view/vehicle/<int:vehicle_id>/',
        views.admin_view_vehicle,
        name='admin_view_vehicle'
    ),
    path(
        'admin/new/vehicle',
        views.admin_create_vehicle_form,
        name='admin_create_vehicle_form'
    ),
    path(
        'admin/edit/vehicle/<int:vehicle_id>/',
        views.admin_edit_vehicle_form,
        name='admin_edit_vehicle_form'
    ),
    path(
        'admin/save/vehicle/',
        views.admin_save_vehicle,
        name='admin_save_vehicle'
    ),
    path(
        'admin/delete/vehicle/<int:vehicle_id>/',
        views.admin_delete_vehicle,
        name='admin_delete_vehicle'
    ),

    # cuenta cliente
    path(
        'client/login/form/',
        views.client_login_form,
        name='client_login_form'
    ),
    path(
        'client/login/',
        views.client_login,
        name='client_login'
    ),
    path(
        'client/signup/form/',
        views.client_signup_form,
        name='client_signup_form'
    ),
    path(
        'client/signup/',
        views.client_signup,
        name='client_signup'
    ),
    path(
        'home/',
        views.home,
        name='home'
    ),
    path(
        'client/rent/list',
        views.client_rent_list,
        name='client_rent_list'
    ),

    # alquiler
    path(
        'rent/request/',
        views.rent_request_form,
        name='rent_request_form'
    ),
    path(
        'rent/select/car/',
        views.rent_select_vehicle,
        name='rent_select_vehicle'
    ),
    path(
        'rent/reserve/car/<int:vehicle_id>/<str:rent_begin>/<str:rent_end>/',
        views.rent_reserve_vehicle_form,
        name='rent_reserve_vehicle_form'
    ),
    path(
        'rent/car/confirm/<int:vehicle_id>/<str:rent_begin>/<str:rent_end>/',
        views.rent_confirm,
        name='rent_confirm'
    ),
    path(
        'rent/car/view/<int:rent_id>/',
        views.rent_view,
        name='rent_view'
    ),
    path(
        'rent/car/cancel/<int:rent_id>/',
        views.rent_cancel,
        name='rent_cancel'
    ),

    path(
        'logout/',
        views.logout_user,
        name='logout'
    )
]
