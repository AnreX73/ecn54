from django.urls import path, include

from ecn.views import *

urlpatterns = [
    path('', index, name='home'),
    path('searched_obj/<str:sale_or_rent>/', searched_obj, name='searched_obj'),
    path('searched_obj/region/<str:sale_or_rent>/<int:city_region>/', searched_obj, name='searched_obj_region'),
    path('searched_obj/obj_type/<str:sale_or_rent>/<int:object_type>/', searched_obj, name='searched_object_type'),
    path('searched_obj/rooms/<str:sale_or_rent>/<int:rooms>/', searched_obj, name='searched_obj_rooms'),
    path('searched_dacha/dacha_type/<int:object_type>/', searched_dacha, name='searched_dacha_type'),
    path('searched_dacha/dacha_distance/<int:city_distance>/', searched_dacha, name='searched_distance'),
    path('show_apartment/<slug:apartment_slug>', show_apartment, name='show_apartment'),
    path('show_dacha/<slug:dacha_slug>', show_dacha, name='show_dacha'),

]

urlpatterns += [
    path('users/', include('django.contrib.auth.urls')),
    path('register/', Register.as_view(), name='register'),
    path('user_login/', UserLogin.as_view(), name='user_login'),
    path('user_password_reset/', UserPasswordReset.as_view(), name='user_password_reset'),
    path('user_password_reset_done/', UserPasswordResetDone.as_view(), name='user_password_reset_done'),
    path('profile/<slug:slug>/', ObjectUpdateView.as_view(), name='object_edit'),
    path('profile/dacha/<slug:slug>/', DachaUpdateView.as_view(), name='dacha_edit'),
    path('<slug:slug>/manage_photos/', manage_photos, name='manage_photos'),
    path('<slug:slug>/manage_out_city_photos/', manage_out_city_photos, name='manage_out_city_photos'),
    path('profile/<slug:slug>/delete/', ObjectDeleteView.as_view(), name='object_delete'),
    path('profile/dacha/<slug:slug>/delete/', DachaDeleteView.as_view(), name='dacha_delete'),
    path('profile/', profile, name='profile'),
    path('add_object/', add_object, name='add_object'),
    path('add_dacha/', add_dacha, name='add_dacha'),
    path('update_user_info/', UpdateUserInfo.as_view(), name='update_user_info'),
]
