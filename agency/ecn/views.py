from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordResetDoneView
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from ecn.models import *
from ecn.slugify import words_to_slug

from ecn.forms import UserCreationForm, UserLoginForm, UserPasswordResetForm, InCitySearchForm, InCityAddForm, \
    ChangeUserlnfoForm, InCityUpdateForm, OutCityAddForm, OutCityUpdateForm, PhotoInlineFormSet2, PhotoInlineFormSet, \
    OutCitySearchForm


def index(request):
    context = {
        'title': 'Агенство ЕЦН',
        'main_page_img': Graphics.objects.get(description='изображение на главную'),
        'main_page_slogan': Graphics.objects.get(description='Слоган'),
        'hot_city_obj': InCityObject.objects.filter(is_hot=True).filter(sale_or_rent='s').select_related('rooms',
                                                                                                         'city_region',
                                                                                                         'object_type').order_by(
            '-time_create'),
        'hot_out_city_obj': OutCityObject.objects.filter(is_hot=True).order_by('-time_create'),
        'hot_title': Graphics.objects.get(description='горячая кнопка на главной'),
        'no_photo': Graphics.objects.get(description='нет фото'),
        'services': Post.objects.all(),
    }
    return render(request, 'ecn/index.html', context=context)


def show_apartment(request, apartment_slug):
    apartment = get_object_or_404(InCityObject, slug=apartment_slug)
    apartment_id = apartment.id
    image = apartment.image
    context = {
        'image': image,
        'apartment': apartment,
        'gallery': Gallery.objects.filter(galleryLink_id=apartment_id),
        'no_photo': Graphics.objects.get(description='нет фото')
    }
    return render(request, 'ecn/apartment.html', context=context)


def show_dacha(request, dacha_slug):
    dacha = get_object_or_404(OutCityObject, slug=dacha_slug)
    dacha_id = dacha.id
    image = dacha.image
    context = {
        'image': image,
        'dacha': dacha,
        'gallery': Gallery2.objects.filter(galleryLink2_id=dacha_id),
        'no_photo': Graphics.objects.get(description='нет фото'),
        'quick_links': OutCityObjectType.objects.all(),

    }
    return render(request, 'ecn/dacha.html', context=context)


def searched_obj(request, **kwargs):
    if request.method == 'POST':
        form = InCitySearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['price']:
                price_filter = form.cleaned_data.pop('price')
            else:
                price_filter = 1000000000
            obj_dic = {k: v for k, v in form.cleaned_data.items() if v is not None}
            selected_items = InCityObject.objects.filter(price__lte=price_filter).filter(**obj_dic).filter(
                is_published=True).order_by('-time_create')

    else:
        selected_items = InCityObject.objects.filter(**kwargs).select_related('city_region', 'rooms',
                                                                              'object_type').order_by('-time_create')
        form = InCitySearchForm(initial=dict(**kwargs))

    context = {
        'title': 'Агенство ЕЦН - поиск',
        'form': form,
        'selected_items': selected_items,
        'no_photo': Graphics.objects.get(description='нет фото'),
    }
    return render(request, 'ecn/searched_obj.html', context=context)


def searched_dacha(request, **kwargs):
    if request.method == 'POST':
        form = OutCitySearchForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['object_type']:
                object_filter = form.cleaned_data['object_type']
            else:
                object_filter = None
            if form.cleaned_data['price']:
                price_filter = form.cleaned_data['price']
            else:
                price_filter = 1000000000
            if form.cleaned_data['city_distance']:
                distance_filter = form.cleaned_data['city_distance'].pk
            else:
                distance_filter = 10
            if form.cleaned_data['land_square']:
                land_square_filter = form.cleaned_data['land_square']
            else:
                land_square_filter = 0

            selected_items = OutCityObject.objects.filter(object_type=object_filter,
                                                          land_square__gte=land_square_filter,
                                                          city_distance__lte=distance_filter,
                                                          price__lte=price_filter).filter(is_published=True).order_by(
                '-time_create')

    else:
        selected_items = OutCityObject.objects.filter(**kwargs).order_by('-time_create')
        form = OutCitySearchForm(initial=dict(**kwargs))

    context = {
        'title': 'Агенство ЕЦН - поиск',
        'form': form,
        'selected_items': selected_items,
        'no_photo': Graphics.objects.get(description='нет фото'),
    }
    return render(request, 'ecn/searched_dacha.html', context=context)


@login_required(login_url='/register/')
def profile(request):
    user = request.user
    context = {
        'user': user,
        'user_city_objects': InCityObject.objects.filter(estate_agent__id=user.id),
        'user_out_city_objects': OutCityObject.objects.filter(estate_agent__id=user.id)
    }
    return render(request, 'registration/profile.html', context=context)


class Register(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm(),
            'title': 'регистрация',
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('profile')
        context = {
            'form': form,
        }
        return render(request, self.template_name, context)


class UpdateUserInfo(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'registration/update_user_info.html'
    form_class = ChangeUserlnfoForm
    success_url = reverse_lazy('profile')
    success_message = 'Данные пользователя изменены'

    def setup(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().setup(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserLogin(SuccessMessageMixin, LoginView):
    template_name = 'registration/user_login.html'
    form_class = UserLoginForm
    success_message = 'Вы авторизованы!'


class UserPasswordReset(PasswordResetView):
    template_name = 'registration/user_password_reset.html'
    form_class = UserPasswordResetForm

    def get_success_url(self):
        return reverse_lazy('user_password_reset_done')


class UserPasswordResetDone(PasswordResetDoneView):
    template_name = 'registration/user_password_reset_done.html'


@login_required(login_url='/register/')
def add_object(request):
    if request.method == 'POST':
        form = InCityAddForm(request.POST, request.FILES)
        if form.is_valid():
            user_valid = form.cleaned_data.get('estate_agent')
            if user_valid == request.user:
                title = form.cleaned_data.get('title')
                new_slug = words_to_slug(title)
                comment = form.save(commit=False)
                comment.is_published = True
                comment.slug = new_slug
                comment.is_hot = False
                comment.save()
            else:
                return redirect('home')
            return redirect('profile')
    else:
        form = InCityAddForm(initial=dict(estate_agent=request.user))

    context = {
        'form': form,
    }

    return render(request, 'registration/add_object.html', context=context)


@login_required(login_url='/register/')
def add_dacha(request):
    if request.method == 'POST':
        form = OutCityAddForm(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data.get('title')
            new_slug = words_to_slug(title)
            comment = form.save(commit=False)
            comment.is_published = True
            comment.slug = new_slug
            comment.is_hot = False
            comment.save()

            return redirect('profile')

    else:
        form = OutCityAddForm(initial=dict(estate_agent=request.user))

    context = {
        'form': form,
    }

    return render(request, 'registration/add_dacha.html', context=context)


class ObjectUpdateView(LoginRequiredMixin, UpdateView):
    model = InCityObject
    template_name = 'registration/update_object.html'
    form_class = InCityUpdateForm


class DachaUpdateView(LoginRequiredMixin, UpdateView):
    model = OutCityObject
    template_name = 'registration/update_dacha.html'
    form_class = OutCityUpdateForm


class ObjectDeleteView(LoginRequiredMixin, DeleteView):
    model = InCityObject
    template_name = 'registration/object_confirm_delete.html'
    success_url = '/profile/'


class DachaDeleteView(LoginRequiredMixin, DeleteView):
    model = OutCityObject
    template_name = 'registration/dacha_confirm_delete.html'
    success_url = '/profile/'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['outcityobjects'] = OutCityObject.objects.all()
        context['no_photo'] = Graphics.objects.get(description='нет фото')
        return context


@login_required(login_url='/register/')
def manage_photos(request, slug):
    parent = get_object_or_404(InCityObject, slug=slug)
    parent_img = Gallery.objects.filter(galleryLink__id=parent.id)
    formset = PhotoInlineFormSet
    if request.method == "POST":
        formset = formset(request.POST, request.FILES, instance=parent)
        if formset.is_valid():
            formset.save()
            return redirect('profile')
    else:
        formset = formset(instance=parent)
    context = {
        'parent': parent,
        'formset': formset,
        'parent_img': parent_img
    }
    return render(request, 'registration/manage_photos.html', context=context)


@login_required(login_url='/register/')
def manage_out_city_photos(request, slug):
    parent = get_object_or_404(OutCityObject, slug=slug)
    parent_img = Gallery2.objects.filter(galleryLink2__id=parent.id)
    formset = PhotoInlineFormSet2
    if request.method == "POST":
        formset = formset(request.POST, request.FILES, instance=parent)
        if formset.is_valid():
            formset.save()
            return redirect('profile')
    else:
        formset = formset(instance=parent)
    context = {
        'parent': parent,
        'formset': formset,
        'parent_img': parent_img
    }
    return render(request, 'registration/manage_out_city_photos.html', context=context)
