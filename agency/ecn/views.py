from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (
    LoginView,
    PasswordResetView,
    PasswordResetDoneView,
)
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from ecn.models import *
from ecn.slugify import words_to_slug
from django.db.models import Min, Max

from ecn.forms import (
    UserCreationForm,
    UserLoginForm,
    UserPasswordResetForm,
    InCityAddForm,
    ChangeUserlnfoForm,
    InCityUpdateForm,
    OutCityAddForm,
    OutCityUpdateForm,
    PhotoInlineFormSet2,
    PhotoInlineFormSet,
    SmartSearchForm,
    SmartSearchRentForm,
    SmartSearchOutForm,
)


def calculate_max_price(selected_items):
    selected_items_max_price = selected_items.aggregate(Max("price"))
    max_price = "{0:,}".format((selected_items_max_price.get("price__max"))).replace(
        ",", "`"
    )
    return max_price


def calculate_min_price(selected_items):
    selected_items_max_price = selected_items.aggregate(Min("price"))
    min_price = "{0:,}".format((selected_items_max_price.get("price__min"))).replace(
        ",", "`"
    )
    return min_price


def index(request):
    context = {
        "title": "Агенство ЕЦН",
        "main_page_img": Graphics.objects.get(description="изображение на главную"),
        "main_page_slogan": Graphics.objects.get(description="Слоган"),
        "hot_city_obj": InCityObject.objects.filter(is_hot=True)
        .filter(sale_or_rent="s")
        .select_related("rooms", "city_region", "object_type")
        .order_by("-time_create")[:6],
        "hot_out_city_obj": OutCityObject.objects.filter(is_hot=True).order_by(
            "-time_create"
        )[:3],
        "hot_title": Graphics.objects.get(description="горячая кнопка на главной"),
        "no_photo": Graphics.objects.get(description="нет фото"),
        "services": Post.objects.all(),
    }
    return render(request, "ecn/index.html", context=context)


def show_apartment(request, apartment_slug):
    apartment = get_object_or_404(InCityObject, slug=apartment_slug)
    apartment_id = apartment.id
    image = apartment.image
    gallery = Gallery.objects.filter(galleryLink_id=apartment_id)
    context = {
        "image": image,
        "apartment": apartment,
        "gallery": gallery,
        "no_photo": Graphics.objects.get(description="нет фото"),
    }
    return render(request, "ecn/apartment.html", context=context)


def show_dacha(request, dacha_slug):
    dacha = get_object_or_404(OutCityObject, slug=dacha_slug)
    dacha_id = dacha.id
    image = dacha.image
    context = {
        "image": image,
        "dacha": dacha,
        "gallery": Gallery2.objects.filter(galleryLink2_id=dacha_id),
        "no_photo": Graphics.objects.get(description="нет фото"),
        "quick_links": OutCityObjectType.objects.all(),
    }
    return render(request, "ecn/dacha.html", context=context)


@login_required(login_url="/register/")
def profile(request):
    user = request.user
    context = {
        "user": user,
        "user_city_objects": InCityObject.objects.filter(estate_agent__id=user.id),
        "user_out_city_objects": OutCityObject.objects.filter(estate_agent__id=user.id),
    }
    return render(request, "registration/profile.html", context=context)


class Register(View):
    template_name = "registration/register.html"

    def get(self, request):
        context = {
            "form": UserCreationForm(),
            "title": "регистрация",
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("profile")
        context = {
            "form": form,
        }
        return render(request, self.template_name, context)


class UpdateUserInfo(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = "registration/update_user_info.html"
    form_class = ChangeUserlnfoForm
    success_url = reverse_lazy("profile")
    success_message = "Данные пользователя изменены"

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserLogin(SuccessMessageMixin, LoginView):
    template_name = "registration/user_login.html"
    form_class = UserLoginForm
    success_message = "Вы авторизованы!"


class UserPasswordReset(PasswordResetView):
    template_name = "registration/user_password_reset.html"
    form_class = UserPasswordResetForm

    def get_success_url(self):
        return reverse_lazy("user_password_reset_done")


class UserPasswordResetDone(PasswordResetDoneView):
    template_name = "registration/user_password_reset_done.html"


@login_required(login_url="/register/")
def add_object(request):
    if request.method == "POST":
        form = InCityAddForm(request.POST, request.FILES)
        if form.is_valid():
            user_valid = form.cleaned_data.get("estate_agent")
            if user_valid == request.user:
                title = form.cleaned_data.get("title")
                new_slug = words_to_slug(title)
                comment = form.save(commit=False)
                comment.is_published = True
                comment.slug = new_slug
                comment.is_hot = False
                comment.save()
            else:
                return redirect("home")
            return redirect("profile")
    else:
        form = InCityAddForm(initial=dict(estate_agent=request.user))

    context = {
        "form": form,
    }

    return render(request, "registration/add_object.html", context=context)


@login_required(login_url="/register/")
def add_dacha(request):
    if request.method == "POST":
        form = OutCityAddForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            new_slug = words_to_slug(title)
            comment = form.save(commit=False)
            comment.is_published = True
            comment.slug = new_slug
            comment.is_hot = False
            comment.save()

            return redirect("profile")

    else:
        form = OutCityAddForm(initial=dict(estate_agent=request.user))

    context = {
        "form": form,
    }

    return render(request, "registration/add_dacha.html", context=context)


class ObjectUpdateView(LoginRequiredMixin, UpdateView):
    model = InCityObject
    template_name = "registration/update_object.html"
    form_class = InCityUpdateForm


class DachaUpdateView(LoginRequiredMixin, UpdateView):
    model = OutCityObject
    template_name = "registration/update_dacha.html"
    form_class = OutCityUpdateForm


class ObjectDeleteView(LoginRequiredMixin, DeleteView):
    model = InCityObject
    template_name = "registration/object_confirm_delete.html"
    success_url = "/profile/"


class DachaDeleteView(LoginRequiredMixin, DeleteView):
    model = OutCityObject
    template_name = "registration/dacha_confirm_delete.html"
    success_url = "/profile/"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["outcityobjects"] = OutCityObject.objects.all()
        context["no_photo"] = Graphics.objects.get(description="нет фото")
        return context


@login_required(login_url="/register/")
def manage_photos(request, slug):
    parent = get_object_or_404(InCityObject, slug=slug)
    parent_img = Gallery.objects.filter(galleryLink__id=parent.id)
    formset = PhotoInlineFormSet
    if request.method == "POST":
        formset = formset(request.POST, request.FILES, instance=parent)
        if formset.is_valid():
            formset.save()
            return redirect("profile")
    else:
        formset = formset(instance=parent)
    context = {"parent": parent, "formset": formset, "parent_img": parent_img}
    return render(request, "registration/manage_photos.html", context=context)


@login_required(login_url="/register/")
def manage_out_city_photos(request, slug):
    parent = get_object_or_404(OutCityObject, slug=slug)
    parent_img = Gallery2.objects.filter(galleryLink2__id=parent.id)
    formset = PhotoInlineFormSet2
    if request.method == "POST":
        formset = formset(request.POST, request.FILES, instance=parent)
        if formset.is_valid():
            formset.save()
            return redirect("profile")
    else:
        formset = formset(instance=parent)
    context = {"parent": parent, "formset": formset, "parent_img": parent_img}
    return render(request, "registration/manage_out_city_photos.html", context=context)


def smart_search(request, **kwargs):

    if request.method == "POST":

        form = SmartSearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["price"]:
                price_filter = form.cleaned_data.pop("price")
            else:
                price_filter = 100_000_000
            obj_dic = {k: v for k, v in form.cleaned_data.items() if v is not None}
            
            selected_items = (
                InCityObject.objects.filter(price__lte=price_filter)
                .filter(sale_or_rent='s')
                .filter(**obj_dic)
                .filter(is_published=True)
                .order_by("-time_create")
            )

            items_count = selected_items.count()
            if items_count > 0:
                min_price = calculate_min_price(selected_items)
                max_price = calculate_max_price(selected_items)
            else:
                min_price = max_price = 0

            context = {
                "title": "Поиск недвижимости",
                "form": form,
                "selected_items": selected_items,
                "no_photo": Graphics.objects.get(description="нет фото"),
                "items_count": items_count,
                "max_price": max_price,
                "min_price": min_price,
            }

        return render(
            request, "ecn/inclusion/smart_searched_objects.html", context=context
        )

    else:
        selected_items = (
            InCityObject.objects.filter(**kwargs)
            .select_related("city_region", "rooms", "object_type")
            .order_by("-time_create")
        )

        items_count = selected_items.count()
        if items_count > 0:
            min_price = calculate_min_price(selected_items)
            max_price = calculate_max_price(selected_items)
        else:
            min_price = max_price = 0
        
        form = SmartSearchForm(initial=dict(**kwargs))

        context = {
            "title": "Поиск недвижимости",
            "form": form,
            "selected_items": selected_items,
            "no_photo": Graphics.objects.get(description="нет фото"),
            "items_count": items_count,
            "max_price": max_price,
            "min_price": min_price,
        }
        return render(request, "ecn/smart_search.html", context=context)


def smart_rent_search(request, **kwargs):

    if request.method == "POST":

        form = SmartSearchRentForm(request.POST)
        if form.is_valid():
            if form.cleaned_data["price"]:
                price_filter = form.cleaned_data.pop("price")
            else:
                price_filter = 1_000_000
            obj_dic = {k: v for k, v in form.cleaned_data.items() if v is not None}

            selected_items = (
                InCityObject.objects.filter(price__lte=price_filter)
                .filter(sale_or_rent='r')
                .filter(**obj_dic)
                .filter(is_published=True)
                .order_by("-time_create")
            )

            items_count = selected_items.count()
            if items_count > 0:
                min_price = calculate_min_price(selected_items)
                max_price = calculate_max_price(selected_items)
            else:
                min_price = max_price = 0

            context = {
                "title": "Поиск недвижимости",
                "form": form,
                "selected_items": selected_items,
                "no_photo": Graphics.objects.get(description="нет фото"),
                "items_count": items_count,
                "max_price": max_price,
                "min_price": min_price,
            }

        return render(
            request, "ecn/inclusion/smart_searched_objects.html", context=context
        )

    else:
        selected_items = (
            InCityObject.objects.filter(**kwargs)
            .select_related("city_region", "rooms", "object_type")
            .order_by("-time_create")
        )

        items_count = selected_items.count()
        if items_count > 0:
            min_price = calculate_min_price(selected_items)
            max_price = calculate_max_price(selected_items)
        else:
            min_price = max_price = 0
        
        form = SmartSearchRentForm(initial=dict(**kwargs))

        context = {
            "title": "Поиск недвижимости",
            "form": form,
            "selected_items": selected_items,
            "no_photo": Graphics.objects.get(description="нет фото"),
            "items_count": items_count,
            "max_price": max_price,
            "min_price": min_price,
        }
        return render(request, "ecn/smart_rent_search.html", context=context)

        
def smart_dacha_search(request, **kwargs):
    if request.method == "POST":
        form = SmartSearchOutForm(request.POST)
        if form.is_valid():

            if form.cleaned_data["price"]:
                price_filter = form.cleaned_data.pop("price")
            else:
                price_filter = 100_000_000
            if form.cleaned_data["land_square"]:
                land_square_filter = form.cleaned_data.pop("land_square")
            else:
                land_square_filter = 100

            if form.cleaned_data["int_city_distance"]:
                distance_filter = form.cleaned_data.pop("int_city_distance")
            else:
                distance_filter = 200
            
            obj_dic = {k: v for k, v in form.cleaned_data.items() if v is not None}

            selected_items = (
                OutCityObject.objects.filter(price__lte=price_filter)
                .filter(land_square__lte=land_square_filter)
                .filter(int_city_distance__lte=distance_filter)
                .filter(**obj_dic)
                .filter(is_published=True)
                .order_by("-time_create")
            )

            items_count = selected_items.count()

            if items_count > 0:
                min_price = calculate_min_price(selected_items)
                max_price = calculate_max_price(selected_items)
            else:
                
                min_price = max_price = 0
            context = {
                "title": "Поиск недвижимости",
                "form": form,
                "selected_items": selected_items,
                "no_photo": Graphics.objects.get(description="нет фото"),
                "items_count": items_count,
                "max_price": max_price,
                "min_price": min_price,
            }

            return render(
                request, "ecn/inclusion/smart_searched_dacha.html", context=context
            )

    else:
        form = SmartSearchOutForm(initial=dict(**kwargs))
        selected_items = OutCityObject.objects.filter(**kwargs).order_by("-time_create")
        items_count = selected_items.count()

        if items_count > 0:
            min_price = calculate_min_price(selected_items)

            max_price = calculate_max_price(selected_items)
        else:
            min_price = max_price = 0

        context = {
            "title": "Поиск недвижимости",
            "form": form,
            "selected_items": selected_items,
            "no_photo": Graphics.objects.get(description="нет фото"),
            "items_count": items_count,
            "max_price": max_price,
            "min_price": min_price,
        }

    return render(request, "ecn/smart_dacha_search.html", context=context)


def commerc_post(request, **kwargs):
    post = Commercial.objects.get(pk=kwargs["id"])
    selected_items = CommercialObject.objects.filter(post_link=post.id)
    no_photo = Graphics.objects.get(description="нет фото")
    items_count = selected_items.count()
    if items_count > 0:
                min_price = calculate_min_price(selected_items)
                max_price = calculate_max_price(selected_items)
    else:
        min_price = max_price = 0
    context = {
        "post": post,
        "title": post.title,
        "selected_items": selected_items,
        'no_photo': no_photo,
        "items_count": items_count,
        "max_price": max_price,
        "min_price": min_price,
    }
    return render(request, "ecn/commerc_post.html", context=context)

def show_commerc_object(request,id):
    commerc_object = get_object_or_404(CommercialObject, id=id)
    commerc_object_id = commerc_object.id
    image = commerc_object.image
    gallery = GalleryComercial.objects.filter(gallery_com_link_id=commerc_object_id)
    context = {
        "image": image,
        "apartment": commerc_object,
        "gallery": gallery,
        "no_photo": Graphics.objects.get(description="нет фото"),
    }
    return render(request, "ecn/commerc_object.html", context=context)
