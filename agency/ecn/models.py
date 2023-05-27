from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from django.urls import reverse


class User(AbstractUser):
    phone_number = models.CharField(max_length=30, blank=True, verbose_name='телефон для связи')

    def get_absolute_url(self):
        return reverse('profile', kwargs={'user_id': self.id})

    def __str__(self):
        return self.username


# тип объекта в городе
class InCityObjectType(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тип объекта')
    slug = models.SlugField(unique=True, max_length=100, db_index=True, verbose_name='URL')
    icon = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, verbose_name='иконка(картинка) для типа объекта')
    in_main_page = models.BooleanField(default=True, verbose_name='в меню на главной странице')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_apartments', kwargs={'obj_type_slug': self.slug})

    def get_rent_url(self):
        return reverse('show_rent', kwargs={'obj_type_slug': self.slug})

    class Meta:
        verbose_name = 'Тип объекта'
        verbose_name_plural = 'Тип объекта'
        ordering = ['id']


# Район города
class InCityRegion(models.Model):
    title = models.CharField(max_length=100, verbose_name='Район города')
    slug = models.SlugField(unique=True, max_length=100, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_region', kwargs={'region_slug': self.slug})

    class Meta:
        verbose_name = 'Район города'
        verbose_name_plural = 'Район города'
        ordering = ['id']


# Станция метро
class MetroStation(models.Model):
    title = models.CharField(max_length=100, verbose_name='Станция метро')
    slug = models.SlugField(unique=True, max_length=100, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('metro', kwargs={'metro_slug': self.slug})

    class Meta:
        verbose_name = 'Станцию метро'
        verbose_name_plural = 'Станция метро'
        ordering = ['id']


# Количество комнат
class RoomAmount(models.Model):
    room_amount = models.PositiveIntegerField(unique=True, verbose_name='Кол-во комнат цифрами')
    title = models.CharField(max_length=25, verbose_name='Количество комнат словами')
    slug = models.SlugField(max_length=150, db_index=True, verbose_name='URL')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('room_amount', kwargs={'rooms_slug': self.slug})

    class Meta:
        verbose_name = 'Количество комнат'
        verbose_name_plural = 'Количество комнат'
        ordering = ['id']


class RoomsLayout(models.Model):
    rooms_layout = models.CharField(max_length=55, verbose_name='Планировка')

    def __str__(self):
        return self.rooms_layout

    class Meta:
        verbose_name = 'Планировка'
        verbose_name_plural = 'Вид планировки'
        ordering = ['id']


# Санузел
class BathroomType(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тип санузла')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип санузла'
        verbose_name_plural = 'Тип санузла'
        ordering = ['id']


# Балкон
class Balcony(models.Model):
    title = models.CharField(max_length=100, verbose_name='Балкон')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Балкон'
        verbose_name_plural = 'Балкон'
        ordering = ['id']


# тип лифта
class ElevatorType(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тип лифта')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Тип лифта'
        verbose_name_plural = 'Тип лифта'
        ordering = ['id']


# состояние объекта
class FlatState(models.Model):
    title = models.CharField(max_length=100, verbose_name='Состояние')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Состояние'
        verbose_name_plural = 'Состояние'
        ordering = ['id']


# тип стройматериалов
class ObjectConstruction(models.Model):
    title = models.CharField(max_length=100, verbose_name='тип стройматериалов')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'тип стройматериалов'
        verbose_name_plural = 'тип стройматериалов'
        ordering = ['id']


# объект городской недвижимости
class InCityObject(models.Model):
    SALE_OR_RENT = (
        ('s', 'Продажа'),
        ('r', 'Аренда')
    )
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, max_length=150, db_index=True, blank=True, verbose_name='URL')
    estate_agent = models.ForeignKey(User, on_delete=models.CASCADE, default=1, blank=True,
                                     verbose_name='агент по недвижимости',
                                     help_text='специалист по объекту', related_name='realtor')
    price = models.PositiveIntegerField(null=True, verbose_name='Цена')
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, verbose_name='Основное изображение')
    sale_or_rent = models.CharField(max_length=25, choices=SALE_OR_RENT, default='s', verbose_name='Продажа или аренда')
    is_hot = models.BooleanField(default=False, verbose_name='горячий вариант', help_text='если хотите видеть на '
                                                                                          'главной странице')
    object_type = models.ForeignKey(InCityObjectType, on_delete=models.PROTECT, verbose_name='тип объекта',
                                    help_text='выберете тип объекта', related_name='obj_type')
    object_adress = models.CharField(max_length=255, blank=True, verbose_name='адрес объекта',
                                     help_text='необязательно')
    city_region = models.ForeignKey(InCityRegion, on_delete=models.PROTECT, verbose_name='район города',
                                    related_name='region')
    metro = models.ForeignKey(MetroStation, on_delete=models.PROTECT, verbose_name='станция метро')
    metro_distance = models.CharField(max_length=255, blank=True, verbose_name='расстояние до метро')
    rooms = models.ForeignKey(RoomAmount, on_delete=models.PROTECT, verbose_name='количество комнат',
                              related_name='rooms')
    square = models.PositiveIntegerField(blank=True, verbose_name='общая площадь кв.м')
    live_square = models.PositiveIntegerField(blank=True, verbose_name='жилая площадь')
    kitchen = models.PositiveIntegerField(blank=True, verbose_name='площадь кухни')
    rooms_layout = models.ForeignKey(RoomsLayout, default=0, on_delete=models.PROTECT, verbose_name='планировка')
    balcony = models.ForeignKey(Balcony, default=2, on_delete=models.PROTECT, verbose_name='балкон')
    floor = models.PositiveIntegerField(blank=True, default=1, verbose_name='Этаж')
    all_floor = models.PositiveIntegerField(blank=True, null=True, verbose_name='Этажность дома')
    bathroom = models.ForeignKey(BathroomType, on_delete=models.PROTECT, verbose_name='санузел')
    elevator = models.ForeignKey(ElevatorType, on_delete=models.PROTECT, verbose_name='лифт')
    state = models.ForeignKey(FlatState, on_delete=models.PROTECT, verbose_name='состояние')
    construction = models.ForeignKey(ObjectConstruction, on_delete=models.PROTECT, verbose_name='тип постройки')
    year = models.CharField(max_length=25, blank=True, verbose_name='Год постройки / Сдачи')
    content = RichTextField(blank=True, verbose_name='текстовое описание ')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_apartment', kwargs={'apartment_slug': self.slug})

    def nice_price(self):
        price = self.price
        nice_price = '{0:,}'.format(price).replace(',', '`')
        return nice_price

    class Meta:
        verbose_name = 'объект'
        verbose_name_plural = 'объект в городе'
        ordering = ['id']


# Тип объекта загородной недвижимости
class OutCityObjectType(models.Model):
    title = models.CharField(max_length=100, verbose_name='Тип загородного объекта')
    slug = models.SlugField(unique=True, max_length=100, db_index=True, verbose_name='URL')
    icon = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, verbose_name='иконка(картинка) для типа объекта')
    in_main_page = models.BooleanField(default=True, verbose_name='в меню на главной странице')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_dachas', kwargs={'obj_type_slug': self.slug})

    class Meta:
        verbose_name = 'Тип загородного объекта'
        verbose_name_plural = 'Тип загородного объекта'
        ordering = ['id']


# расстояние до города
class DistanceToCity(models.Model):
    distance = models.CharField(max_length=255, null=True, verbose_name='Расстояние до города')

    def __str__(self):
        return self.distance

    class Meta:
        verbose_name = 'Расстояние до города'
        verbose_name_plural = 'Расстояние до города'
        ordering = ['id']


# форма собственности
class TypeOfOwnership(models.Model):
    title = models.CharField(max_length=155, verbose_name='форма собственности')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'форму собственности'
        verbose_name_plural = 'форма собственности'
        ordering = ['id']


# электроснабжение
class Electricity(models.Model):
    title = models.CharField(max_length=55, verbose_name='Электроснабжение')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Электроснабжение'
        verbose_name_plural = 'Электроснабжение'
        ordering = ['id']


# вода
class Water(models.Model):
    title = models.CharField(max_length=55, verbose_name='Вода')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Вода'
        verbose_name_plural = 'Вода'
        ordering = ['id']


# газ
class Gas(models.Model):
    title = models.CharField(max_length=55, verbose_name='Газ')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Газ'
        verbose_name_plural = 'Газ'
        ordering = ['id']


# посадки
class Landings(models.Model):
    title = models.CharField(max_length=55, verbose_name='Посадки')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Посадки'
        verbose_name_plural = 'Посадки'
        ordering = ['id']


# баня
class Bath(models.Model):
    title = models.CharField(max_length=55, verbose_name='Баня')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Баня'
        verbose_name_plural = 'Баня'
        ordering = ['id']


# Гараж
class Garage(models.Model):
    title = models.CharField(max_length=55, verbose_name='Гараж')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Гараж'
        verbose_name_plural = 'Гараж'
        ordering = ['id']


# Теплица
class Greenhouse(models.Model):
    title = models.CharField(max_length=55, verbose_name='Теплица')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Теплица'
        verbose_name_plural = 'Теплица'
        ordering = ['id']


# Охрана
class Security(models.Model):
    title = models.CharField(max_length=55, verbose_name='Охрана')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Охрана'
        verbose_name_plural = 'Охрана'
        ordering = ['id']


# Асфальтовая дорога
class GoodRoad(models.Model):
    title = models.CharField(max_length=55, verbose_name='Асфальтовая дорога')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Асфальтовая дорога'
        verbose_name_plural = 'Асфальтовая дорога'
        ordering = ['id']


# Доступ зимой
class WinterAccess(models.Model):
    title = models.CharField(max_length=55, verbose_name='Доступ зимой')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Доступ зимой'
        verbose_name_plural = 'Доступ зимой'
        ordering = ['id']


# Магазин рядом
class ShopNearly(models.Model):
    title = models.CharField(max_length=55, verbose_name='Магазин рядом')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Магазин рядом'
        verbose_name_plural = 'Магазин рядом'
        ordering = ['id']


# Водоем рядом
class WaterNearly(models.Model):
    title = models.CharField(max_length=55, verbose_name='Водоем рядом')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Водоем рядом'
        verbose_name_plural = 'Водоем рядом'
        ordering = ['id']


# Лес рядом
class ForestNearly(models.Model):
    title = models.CharField(max_length=55, verbose_name='Лес рядом')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Лес рядом'
        verbose_name_plural = 'Лес рядом'
        ordering = ['id']


# объект загородной недвижимости
class OutCityObject(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, max_length=150, db_index=True, verbose_name='URL')
    estate_agent = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='агент по недвижимости',
                                     help_text='специалист по объекту', related_name='estate_agent')
    price = models.PositiveIntegerField(null=True, verbose_name='Цена')
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, verbose_name='Основное изображение')
    is_hot = models.BooleanField(default=False, verbose_name='горячий вариант')
    object_type = models.ForeignKey(OutCityObjectType, on_delete=models.PROTECT, verbose_name='тип объекта',
                                    related_name='obj_type')
    object_adress = models.CharField(max_length=255, blank=True, verbose_name='адрес объекта')
    city_distance = models.ForeignKey(DistanceToCity, on_delete=models.PROTECT, null=True,
                                      verbose_name='расстояние до города')
    land_square = models.PositiveIntegerField(blank=True, verbose_name='площадь участка')
    type_of_ownership = models.ForeignKey(TypeOfOwnership, on_delete=models.PROTECT, verbose_name='форма собственности')
    square = models.PositiveIntegerField(blank=True, verbose_name='площадь дома', help_text='в кв.м')
    year = models.CharField(max_length=25, blank=True, verbose_name='год постройки')
    construction = models.ForeignKey(ObjectConstruction, on_delete=models.PROTECT, verbose_name='тип постройки')
    state = models.ForeignKey(FlatState, on_delete=models.PROTECT, verbose_name='состояние')
    bathroom = models.ForeignKey(BathroomType, on_delete=models.PROTECT, verbose_name='Туалет')
    electricity = models.ForeignKey(Electricity, on_delete=models.PROTECT, verbose_name='Электричество')
    gas = models.ForeignKey(Gas, on_delete=models.PROTECT, verbose_name='Газ')
    water = models.ForeignKey(Water, on_delete=models.PROTECT, verbose_name='Вода')
    bath = models.ForeignKey(Bath, on_delete=models.PROTECT, verbose_name='Баня')
    garage = models.ForeignKey(Garage, on_delete=models.PROTECT, verbose_name='Гараж')
    landings = models.ForeignKey(Landings, on_delete=models.PROTECT, verbose_name='Посадки')
    greenhouse = models.ForeignKey(Greenhouse, on_delete=models.PROTECT, verbose_name='Теплица')
    security = models.ForeignKey(Security, on_delete=models.PROTECT, verbose_name='Охрана')
    good_road = models.ForeignKey(GoodRoad, on_delete=models.PROTECT, verbose_name='Асфальтовая дорога')
    winter_access = models.ForeignKey(WinterAccess, on_delete=models.PROTECT, verbose_name='Доступ зимой')
    shop_nearly = models.ForeignKey(ShopNearly, on_delete=models.PROTECT, verbose_name='Магазин рядом')
    water_nearly = models.ForeignKey(WaterNearly, on_delete=models.PROTECT, verbose_name='Водоем рядом')
    forest_nearly = models.ForeignKey(ForestNearly, on_delete=models.PROTECT, verbose_name='Лес рядом')
    transport_distance = models.CharField(max_length=255, blank=True, verbose_name='расстояние до транспорта')
    content = RichTextField(blank=True, verbose_name='текстовое описание')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_dacha', kwargs={'dacha_slug': self.slug})

    def nice_price(self):
        price = self.price
        nice_price = '{0:,}'.format(price).replace(',', '`')
        return nice_price

    class Meta:
        verbose_name = 'Загородный объект'
        verbose_name_plural = 'Загородный объект'
        ordering = ['id']


# Графические объекты и прочее на сайте
class Graphics(models.Model):
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, verbose_name='изображение')
    description = models.CharField(max_length=55, verbose_name='описание изображения')
    note = RichTextField(blank=True, verbose_name='примечание')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    def __str__(self):
        return self.description

    class Meta:
        verbose_name = 'графический объект'
        verbose_name_plural = 'Графика и т.п.'
        ordering = ['id']


# Статьи
class Post(models.Model):
    title = models.CharField(max_length=55, verbose_name='Заголовок статьи')
    content = RichTextField(blank=True, verbose_name='текст статьи')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Статью'
        verbose_name_plural = 'Статьи'
        ordering = ['id']


# Галереи фото квартир
class Gallery(models.Model):
    galleryLink = models.ForeignKey(InCityObject, on_delete=models.CASCADE, verbose_name='Ссылка на объект')
    gallery_image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, null=True, verbose_name='Фото')
    note = models.CharField(blank=True, max_length=100, verbose_name='примечание')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    def __str__(self):
        return self.note

    class Meta:
        verbose_name = 'фотографию объекта'
        verbose_name_plural = 'фото объекта'
        ordering = ['galleryLink']


# Галерея фото загородной недвижимости
class Gallery2(models.Model):
    galleryLink2 = models.ForeignKey(OutCityObject, on_delete=models.CASCADE, verbose_name='Ссылка на объект')
    gallery_image2 = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, verbose_name='Фото')
    note2 = models.CharField(blank=True, max_length=100, verbose_name='примечание')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    def __str__(self):
        return self.note2

    class Meta:
        verbose_name = 'фото объекта'
        verbose_name_plural = 'фото загородного объекта'
        ordering = ['galleryLink2']


class Commercial(models.Model):
    title = models.CharField(blank=True, max_length=255, verbose_name='Заголовок')
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, null=True, verbose_name='иллюстрация')
    video = models.FileField(upload_to='images/%Y/%m/%d', blank=True, null=True, verbose_name='видео (если есть)')
    post = RichTextField(blank=True, verbose_name='рекламная статья')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_commercial', kwargs={'pk': self.id})

    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Рекламные статьи'
        ordering = ['id']


class CommercialObject(models.Model):
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    estate_agent = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, verbose_name='агент по недвижимости',
                                     help_text='специалист по объекту', related_name='com_agent')
    post_link = models.ForeignKey(Commercial, on_delete=models.CASCADE, verbose_name='ссылка на статью',
                                  related_name='commercial_link')
    price = models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Цена')
    image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, null=True, verbose_name='Основное изображение')
    object_adress = models.CharField(max_length=255, blank=True, verbose_name='адрес объекта',
                                     help_text='необязательно')
    city_region = models.ForeignKey(InCityRegion, on_delete=models.PROTECT, verbose_name='район города',
                                    related_name='region_of_city')
    rooms = models.ForeignKey(RoomAmount, on_delete=models.PROTECT, verbose_name='количество комнат',
                              related_name='rooms_amount')
    square = models.PositiveIntegerField(blank=True, verbose_name='общая площадь кв.м')
    live_square = models.PositiveIntegerField(blank=True, verbose_name='жилая площадь')
    kitchen = models.PositiveIntegerField(blank=True, verbose_name='площадь кухни')
    floor = models.PositiveIntegerField(blank=True, default=1, verbose_name='Этаж')
    all_floor = models.PositiveIntegerField(blank=True, null=True, verbose_name='Этажность дома')
    bathroom = models.ForeignKey(BathroomType, on_delete=models.PROTECT, verbose_name='санузел')
    elevator = models.ForeignKey(ElevatorType, on_delete=models.PROTECT, verbose_name='лифт')
    construction = models.ForeignKey(ObjectConstruction, on_delete=models.PROTECT, verbose_name='тип постройки')
    year = models.CharField(max_length=25, blank=True, verbose_name='Год постройки / Сдачи')
    content = RichTextField(blank=True, verbose_name='текстовое описание ')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время изменения')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('show_obj', kwargs={'pk': self.id})

    def nice_price(self):
        price = self.price
        nice_price = '{0:,}'.format(price).replace(',', '`')
        return nice_price

    class Meta:
        verbose_name = 'рекламный объект'
        verbose_name_plural = 'Рекламные объекты'
        ordering = ['id']


class GalleryComercial(models.Model):
    gallery_com_link = models.ForeignKey(CommercialObject, on_delete=models.CASCADE, verbose_name='Ссылка на объект')
    com_image = models.ImageField(upload_to='images/%Y/%m/%d', blank=True, verbose_name='Фото')
    note = models.CharField(blank=True, max_length=100, verbose_name='примечание')
    is_published = models.BooleanField(default=True, verbose_name='Публикация')

    def __str__(self):
        return self.note

    class Meta:
        verbose_name = 'фото комерческого объекта'
        verbose_name_plural = 'фото комерческих объектов'
        ordering = ['gallery_com_link']
