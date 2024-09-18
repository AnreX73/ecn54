from django.urls import path, include

from ecn.views import *

urlpatterns = [
    path("", index, name="home"),
    
    path("show_apartment/<slug:apartment_slug>", show_apartment, name="show_apartment"),
    path("show_dacha/<slug:dacha_slug>", show_dacha, name="show_dacha"),

    path("smart_search/", smart_search, name="smart_search"),
    path("smart_search/<str:sale_or_rent>/<int:object_type>/", smart_search, name="search_object_type"),
    path("smart_search/<str:sale_or_rent>/", smart_search, name="search_sale_or_rent"),
    path("smart_search/rooms/<str:sale_or_rent>/<int:rooms>/", smart_search, name="search_obj_rooms"),
    path("smart_search/region/<str:sale_or_rent>/<int:city_region>/", smart_search, name="search_obj_region"),
    path("smart_dacha_search/", smart_dacha_search, name="smart_dacha_search"),
    path("smart_dacha_search/<int:object_type>/", smart_dacha_search, name="smart_dacha_obj_type"),
    

    path("smart_rent_search/", smart_rent_search, name="smart_rent_search"),
    path("smart_rent_search/<str:sale_or_rent>/", smart_rent_search, name="search_rent_sale_or_rent"),
    path("smart_rent_search/region/<str:sale_or_rent>/<int:city_region>/", smart_rent_search, name="search_rent_obj_region"),
    path("smart_rent_search/region/<str:sale_or_rent>/<int:city_region>/", smart_rent_search, name="search_rent_obj_region"),
    path("smart_rent_search/<str:sale_or_rent>/<int:object_type>/", smart_rent_search, name="search_rent_object_type"),
    path("commerc_post/<int:id>/", commerc_post, name="commerc-post"),
]

urlpatterns += [
    path("users/", include("django.contrib.auth.urls")),
    path("register/", Register.as_view(), name="register"),
    path("vhod/", UserLogin.as_view(), name="user_login"),
    path(
        "user_password_reset/", UserPasswordReset.as_view(), name="user_password_reset"
    ),
    path(
        "user_password_reset_done/",
        UserPasswordResetDone.as_view(),
        name="user_password_reset_done",
    ),
    path("profile/<slug:slug>/", ObjectUpdateView.as_view(), name="object_edit"),
    path("profile/dacha/<slug:slug>/", DachaUpdateView.as_view(), name="dacha_edit"),
    path("<slug:slug>/manage_photos/", manage_photos, name="manage_photos"),
    path(
        "<slug:slug>/manage_out_city_photos/",
        manage_out_city_photos,
        name="manage_out_city_photos",
    ),
    path(
        "profile/<slug:slug>/delete/", ObjectDeleteView.as_view(), name="object_delete"
    ),
    path(
        "profile/dacha/<slug:slug>/delete/",
        DachaDeleteView.as_view(),
        name="dacha_delete",
    ),
    path("profile/", profile, name="profile"),
    path("add_object/", add_object, name="add_object"),
    path("add_dacha/", add_dacha, name="add_dacha"),
    path("update_user_info/", UpdateUserInfo.as_view(), name="update_user_info"),
]
