from django.contrib.auth import get_user_model
from django.contrib.auth.forms import (
    UserCreationForm,
    AuthenticationForm,
    PasswordResetForm,
)
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _
from ckeditor.widgets import CKEditorWidget
from captcha.fields import CaptchaField
from pilkit.processors import ResizeToFill, ResizeToCover
from django.db.models import Min, Max

from ecn.models import InCityObject, OutCityObject, Gallery, Gallery2, RoomsLayout
from imagekit.forms import ProcessedImageField

from pilkit.lib import Image

User = get_user_model()

get_max_price = InCityObject.objects.aggregate(Max("price"))
max_price = get_max_price.get("price__max")

get_max_rent_price = InCityObject.objects.filter(sale_or_rent="r").aggregate(
    Max("price")
)
max_rent_price = get_max_rent_price.get("price__max")
get_dacha_price = OutCityObject.objects.aggregate(Max("price"))
max_dacha_price = get_dacha_price.get("price__max")

get_max_land_square = OutCityObject.objects.aggregate(Max("land_square"))
max_land_square = get_max_land_square.get("land_square__max")


class UserCreationForm(UserCreationForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "class": "form-input"}),
    )
    first_name = forms.CharField(
        label=_("first name"),
        max_length=150,
        required=True,
        help_text="Как к Вам обращаться?",
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    phone_number = forms.CharField(
        label="телефон для связи",
        max_length=15,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    password1 = forms.CharField(
        label=_("password"),
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
    )
    password2 = forms.CharField(
        label="повтор пароля",
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
    )
    captcha = CaptchaField(label="Введите текст с картинки")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "phone_number")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-input"}),
        }


class ChangeUserlnfoForm(forms.ModelForm):
    phone_number = forms.CharField(
        label="телефон для связи",
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email", "first_name", "phone_number")
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-input"}),
            "email": forms.EmailInput(attrs={"class": "form-input"}),
            "first_name": forms.TextInput(attrs={"class": "form-input"}),
        }


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )
    password = forms.CharField(
        label=_("password"),
        widget=forms.PasswordInput(attrs={"class": "form-input"}),
    )
    # captcha = CaptchaField(label='Введите текст с картинки')


class UserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        label=_("Email"),
        max_length=254,
        widget=forms.EmailInput(attrs={"autocomplete": "email", "class": "form-input"}),
    )


class InCitySearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["city_region"].empty_label = "все районы"
        self.fields["object_type"].empty_label = "все предложения"
        self.fields["rooms"].empty_label = "любое"
        self.fields["rooms"].required = False
        self.fields["city_region"].required = False
        self.fields["object_type"].required = False
        self.fields["price"].required = False

    price = forms.IntegerField(
        min_value=0,
        label="Цена не выше",
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "цифры(без пробелов)", "class": "form-input"}
        ),
    )

    class Meta:
        model = InCityObject
        fields = ("sale_or_rent", "object_type", "price", "city_region", "rooms")


class OutCitySearchForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["city_distance"].empty_label = "любая удаленность"
        self.fields["land_square"].required = False
        self.fields["city_distance"].required = False
        self.fields["object_type"].required = False
        self.fields["price"].required = False

    land_square = forms.IntegerField(
        min_value=0,
        label="Площадь участка",
        widget=forms.widgets.NumberInput(
            attrs={"placeholder": "не менее (в сотках)", "class": "form-input"}
        ),
    )
    price = forms.IntegerField(
        min_value=0,
        label="Цена не выше",
        widget=forms.widgets.NumberInput(
            attrs={"placeholder": "цифры(без пробелов)", "class": "form-input"}
        ),
    )

    class Meta:
        model = OutCityObject
        fields = ("object_type", "price", "city_distance", "land_square")


class InCityAddForm(forms.ModelForm):
    title = forms.CharField(
        label="Заголовок",
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "краткое название", "class": "form-input"}
        ),
    )
    price = forms.IntegerField(
        label="Цена",
        widget=forms.widgets.NumberInput(
            attrs={"placeholder": "только цифры(без пробелов)", "class": "form-input"}
        ),
    )
    object_adress = forms.CharField(
        label="Адрес",
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "кратко (улица, номер дома)", "class": "form-input"}
        ),
    )
    metro_distance = forms.CharField(
        label="Расстояние до метро",
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "кратко", "class": "form-input"}
        ),
    )
    rooms_layout = forms.ModelChoiceField(
        queryset=RoomsLayout.objects.all(), label="Планировка"
    )
    square = forms.IntegerField(
        label="Общая площадь",
        widget=forms.widgets.NumberInput(
            attrs={"placeholder": "только цифры(без пробелов)", "class": "form-input"}
        ),
    )
    live_square = forms.IntegerField(
        label="Жилая площадь",
        widget=forms.widgets.NumberInput(
            attrs={"placeholder": "только цифры(без пробелов)", "class": "form-input"}
        ),
    )
    kitchen = forms.IntegerField(
        label="Площадь кухни",
        widget=forms.widgets.NumberInput(
            attrs={"placeholder": "только цифры(без пробелов)", "class": "form-input"}
        ),
    )
    slug = forms.CharField(widget=forms.HiddenInput, label="")
    is_hot = forms.CharField(widget=forms.HiddenInput, label="")
    is_published = forms.CharField(widget=forms.HiddenInput, label="")
    estate_agent = forms.ModelChoiceField(
        queryset=User.objects.all(), widget=forms.HiddenInput, label=""
    )
    content = forms.CharField(widget=CKEditorWidget, label="Текстовое описание")
    image = ProcessedImageField(
        spec_id="ecn:media:ecn_thumbnail",
        label="Основное изображение",
        processors=[ResizeToCover(1200, 900)],
        format="JPEG",
        options={"quality": 70},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].required = False
        self.fields["is_hot"].required = False
        self.fields["is_published"].required = False

    class Meta:
        model = InCityObject
        fields = "__all__"


class InCityUpdateForm(InCityAddForm):
    image = ProcessedImageField(
        spec_id="ecn:media:ecn_thumbnail",
        label="Изменить изображение",
        processors=[ResizeToCover(1200, 900)],
        format="JPEG",
        options={"quality": 70},
        validators=[
            validators.FileExtensionValidator(allowed_extensions=("gif", "jpg", "png"))
        ],
        error_messages={"invalid_extension": "Этот формат не поддерживается"},
        widget=forms.widgets.FileInput,
    )


class OutCityAddForm(forms.ModelForm):
    title = forms.CharField(
        label="Заголовок",
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "краткое название", "class": "form-input"}
        ),
    )
    price = forms.IntegerField(
        label="Цена",
        widget=forms.widgets.NumberInput(
            attrs={"placeholder": "только цифры(без пробелов)", "class": "form-input"}
        ),
    )
    object_adress = forms.CharField(
        label="Адрес",
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "кратко (улица, номер дома)", "class": "form-input"}
        ),
    )
    land_square = forms.IntegerField(
        label="Площадь участка",
        widget=forms.widgets.NumberInput(
            attrs={"placeholder": "в сотках(только цифры)", "class": "form-input"}
        ),
    )
    transport_distance = forms.CharField(
        label="Расстояние до транспорта",
        widget=forms.widgets.TextInput(
            attrs={"placeholder": "кратко", "class": "form-input"}
        ),
    )
    square = forms.IntegerField(
        label="Площадь дома",
        widget=forms.widgets.NumberInput(
            attrs={"placeholder": "если он есть", "class": "form-input"}
        ),
    )
    slug = forms.CharField(widget=forms.HiddenInput, label="")
    is_hot = forms.CharField(widget=forms.HiddenInput, label="")
    is_published = forms.CharField(widget=forms.HiddenInput, label="")
    estate_agent = forms.ModelChoiceField(
        queryset=User.objects.all(), widget=forms.HiddenInput, label=""
    )
    content = forms.CharField(widget=CKEditorWidget, label="Текстовое описание")
    image = ProcessedImageField(
        spec_id="ecn:media:ecn_thumbnail",
        label="Основное изображение",
        processors=[ResizeToCover(1200, 900)],
        format="JPEG",
        options={"quality": 70},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["slug"].required = False
        self.fields["is_hot"].required = False
        self.fields["is_published"].required = False

    class Meta:
        model = OutCityObject
        fields = "__all__"


class OutCityUpdateForm(OutCityAddForm):
    image = ProcessedImageField(
        spec_id="ecn:media:ecn_thumbnail",
        label="Изменить изображение",
        processors=[ResizeToCover(1200, 900)],
        format="JPEG",
        options={"quality": 70},
        validators=[
            validators.FileExtensionValidator(allowed_extensions=("gif", "jpg", "png"))
        ],
        error_messages={"invalid_extension": "Этот формат не поддерживается"},
        widget=forms.widgets.FileInput,
    )


class PhotoAddForm(forms.ModelForm):
    gallery_image = ProcessedImageField(
        spec_id="ecn:media:ecn_thumbnail",
        label="Изменить / добавить  изображение",
        processors=[ResizeToCover(1200, 900)],
        format="JPEG",
        options={"quality": 70},
        validators=[
            validators.FileExtensionValidator(
                allowed_extensions=("gif", "jpg", "jpeg", "png")
            )
        ],
        error_messages={"invalid_extension": "Этот формат не поддерживается"},
        required=False,
        widget=forms.widgets.FileInput,
    )

    is_published = forms.CharField(
        widget=forms.HiddenInput, label="", required=False, initial=True
    )
    note = forms.CharField(
        label="примечание (не обязательно)",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )


PhotoInlineFormSet = inlineformset_factory(
    InCityObject, Gallery, form=PhotoAddForm, fields="__all__", extra=9, max_num=10
)


class PhotoAddForm2(forms.ModelForm):
    gallery_image2 = ProcessedImageField(
        spec_id="ecn:media:ecn_thumbnail",
        label="Изменить / добавить  изображение",
        processors=[ResizeToFill(1200, 900)],
        format="JPEG",
        options={"quality": 70},
        validators=[
            validators.FileExtensionValidator(
                allowed_extensions=("gif", "jpg", "jpeg", "png")
            )
        ],
        error_messages={"invalid_extension": "Этот формат не поддерживается"},
        required=False,
        widget=forms.widgets.FileInput,
    )

    is_published = forms.CharField(
        widget=forms.HiddenInput, label="", required=False, initial=True
    )
    note2 = forms.CharField(
        label="примечание (не обязательно)",
        required=False,
        widget=forms.TextInput(attrs={"class": "form-input"}),
    )


PhotoInlineFormSet2 = inlineformset_factory(
    OutCityObject, Gallery2, form=PhotoAddForm2, fields="__all__", extra=9, max_num=10
)


htmx_url = "/smart_search/"
htmx_dacha_url = "/smart_dacha_search/"
range_widget = forms.widgets.NumberInput(
    attrs={
        "type": "range",
        "step": "100000",
        "min": "0",
        "max": max_price,
        "id": "myRange",
        "value": max_price,
        "hx-post": htmx_url,
        "hx-trigger": "change delay:500ms",
        "hx-target": "#search-results",
        "hx-swap": "innerHTML",
        "hx-push-url": "/smart_search/",
    }
)
dacha_range_widget = forms.widgets.NumberInput(
    attrs={
        "type": "range",
        "step": "100000",
        "min": "0",
        "max": max_dacha_price,
        "id": "myRange",
        "value": max_dacha_price,
        "hx-post": htmx_dacha_url,
        "hx-trigger": "change delay:500ms",
        "hx-target": "#search-results",
        "hx-swap": "innerHTML",
        "hx-push-url": htmx_dacha_url,
    }
)
micro_range_widget = forms.widgets.NumberInput(
    attrs={
        "type": "range",
        "step": "1",
        "min": "0",
        "max": max_land_square,
        "id": "mySquareRange",
        "value": max_land_square,
        "hx-post": htmx_dacha_url,
        "hx-trigger": "change delay:500ms",
        "hx-target": "#search-results",
        "hx-swap": "innerHTML",
        "hx-push-url": htmx_dacha_url,
    }
)
little_range_widget = forms.widgets.NumberInput(
    attrs={
        "type": "range",
        "step": "500",
        "min": "0",
        "max": max_rent_price,
        "id": "myRange",
        "value": max_rent_price,
        "hx-post": htmx_url,
        "hx-trigger": "change delay:500ms",
        "hx-target": "#search-results",
        "hx-swap": "innerHTML",
        "hx-push-url": "/smart_search/",
    }
)
search_widjets = {
    "object_type": forms.widgets.Select(
        attrs={
            "hx-post": htmx_url,
            "hx-trigger": "change",
            "hx-target": "#search-results",
            "hx-swap": "innerHTML",
            "hx-push-url": htmx_url,
        }
    ),
    "city_region": forms.widgets.Select(
        attrs={
            "hx-post": htmx_url,
            "hx-trigger": "change",
            "hx-target": "#search-results",
            "hx-swap": "innerHTML",
            "hx-push-url": htmx_url,
        }
    ),
    "sale_or_rent": forms.widgets.Select(
        attrs={
            "onchange": "this.form.submit()",
        }
    ),
    "rooms": forms.widgets.Select(
        attrs={
            "hx-post": htmx_url,
            "hx-trigger": "change ",
            "hx-target": "#search-results",
            "hx-swap": "innerHTML",
            "hx-push-url": htmx_url,
        }
    ),
}


class SmartSearchForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["sale_or_rent"].required = False
        self.fields["city_region"].required = False
        self.fields["object_type"].required = False
        self.fields["price"].required = False
        self.fields["rooms"].required = False
        self.fields["city_region"].empty_label = "все районы"
        self.fields["object_type"].empty_label = "все предложения"
        self.fields["rooms"].empty_label = "любое"

    class Meta:
        model = InCityObject
        fields = ("sale_or_rent", "city_region", "object_type", "price", "rooms")
        widgets = search_widjets
        search_widjets["price"] = range_widget


class SmartSearchRentForm(SmartSearchForm):
    class Meta:
        model = InCityObject
        fields = ("sale_or_rent", "city_region", "object_type", "price", "rooms")
        widgets = search_widjets
        search_widjets["price"] = little_range_widget



search_dacha_widjets = {
    "object_type": forms.widgets.Select(
        attrs={
            "hx-post": htmx_dacha_url,
            "hx-trigger": "change",
            "hx-target": "#search-results",
            "hx-swap": "innerHTML",
            "hx-push-url": htmx_dacha_url,
        }
    ),
    "city_distance": forms.widgets.Select(
        attrs={
            "hx-post": htmx_dacha_url,
            "hx-trigger": "change",
            "hx-target": "#search-results",
            "hx-swap": "innerHTML",
            "hx-push-url": htmx_dacha_url,
            
        }
    ),
   
}
class SmartSearchOutForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["object_type"].empty_label = "все предложения"
        self.fields["city_distance"].empty_label = "не имеет значения"
        self.fields["object_type"].required = False
        self.fields["price"].required = False
        self.fields["city_distance"].required = False
        self.fields["land_square"].required = False

    class Meta:
        model = OutCityObject
        fields = ("object_type", "price", "city_distance", "land_square")
        widgets = search_dacha_widjets
        search_dacha_widjets["price"] = dacha_range_widget
        search_dacha_widjets["land_square"] = micro_range_widget
