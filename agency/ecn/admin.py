from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.utils.safestring import mark_safe

from ecn.models import *

User = get_user_model()


@admin.register(User)
class UserAdmin(UserAdmin):
    pass


@admin.register(InCityObjectType)
class InCityObjectTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'gethtmlPhoto', 'title', 'slug')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True

    def gethtmlPhoto(self, picture):
        if picture.icon:
            return mark_safe(f"<img src='{picture.icon.url}' width=50>")

    gethtmlPhoto.short_description = 'миниатюра'


@admin.register(InCityRegion)
class InCityRegionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True


@admin.register(MetroStation)
class MetroStationAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True


@admin.register(RoomAmount)
class RoomAmountAdmin(admin.ModelAdmin):
    list_display = ('id', 'room_amount', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True


@admin.register(RoomsLayout)
class RoomsLayoutAdmin(admin.ModelAdmin):
    list_display = ('id', 'rooms_layout')
    list_display_links = ('id', 'rooms_layout')
    search_fields = ('rooms_layout',)
    save_on_top = True


@admin.register(BathroomType)
class BathroomTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(ElevatorType)
class ElevatorTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(FlatState)
class FlatStateAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(ObjectConstruction)
class ObjectConstructionAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(Balcony)
class BalconyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


class GalleryAdmin(admin.TabularInline):
    model = Gallery
    fields = ('gallery_image', 'gethtmlPhoto', 'note', 'is_published')
    readonly_fields = ('gethtmlPhoto',)

    def gethtmlPhoto(self, picture):
        if picture.gallery_image:
            return mark_safe(f"<img src='{picture.gallery_image.url}' width=75>")

    gethtmlPhoto.short_description = 'миниатюра'


class InCityObjectAdmin(admin.ModelAdmin):
    inlines = [GalleryAdmin]
    list_display = (
        'sale_or_rent', 'title', 'estate_agent', 'gethtmlPhoto', 'city_region', 'price', 'object_type', 'is_published')
    list_display_links = ('sale_or_rent', 'title')
    search_fields = ('title', 'rooms', 'city_region',)
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create', 'estate_agent')
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True

    def gethtmlPhoto(self, picture):
        if picture.image:
            return mark_safe(f"<img src='{picture.image.url}' width=50>")

    gethtmlPhoto.short_description = 'миниатюра'


class GalleryAdmin2(admin.TabularInline):
    model = Gallery2
    fields = ('gallery_image2', 'gethtmlPhoto', 'note2', 'is_published')
    readonly_fields = ('gethtmlPhoto',)

    def gethtmlPhoto(self, picture):
        if picture.gallery_image2:
            return mark_safe(f"<img src='{picture.gallery_image2.url}' width=75>")

    gethtmlPhoto.short_description = 'миниатюра'


class OutCityObjectAdmin(admin.ModelAdmin):
    inlines = [GalleryAdmin2]
    list_display = (
        'id', 'title', 'gethtmlPhoto', 'estate_agent', 'object_adress', 'land_square', 'price', 'is_published')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'land_square',)
    list_editable = ('is_published',)
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('is_published', 'time_create')
    save_on_top = True

    def gethtmlPhoto(self, picture):
        if picture.image:
            return mark_safe(f"<img src='{picture.image.url}' width=50>")

    gethtmlPhoto.short_description = 'миниатюра'


@admin.register(OutCityObjectType)
class OutCityObjectTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'gethtmlPhoto', 'title', 'slug')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    prepopulated_fields = {'slug': ('title',)}
    save_on_top = True

    def gethtmlPhoto(self, picture):
        if picture.icon:
            return mark_safe(f"<img src='{picture.icon.url}' width=50>")

    gethtmlPhoto.short_description = 'миниатюра'


@admin.register(TypeOfOwnership)
class TypeOfOwnershipAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(DistanceToCity)
class DistanceToCityAdmin(admin.ModelAdmin):
    list_display = ('id', 'distance')
    list_display_links = ('id', 'distance')
    search_fields = ('distance',)
    save_on_top = True


@admin.register(Electricity)
class ElectricityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(Water)
class WaterAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(Gas)
class GasAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(Bath)
class BathAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(Landings)
class LandingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(Garage)
class GarageAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(Greenhouse)
class GreenhouseAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(Security)
class SecurityAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(GoodRoad)
class GoodRoadAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(WinterAccess)
class WinterAccessAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(ShopNearly)
class ShopNearlyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(WaterNearly)
class WaterNearlyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(ForestNearly)
class ForestNearlyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(Graphics)
class GraphicsAdmin(admin.ModelAdmin):
    list_display = ('id', 'gethtmlPhoto', 'description', 'note', 'is_published')
    list_display_links = ('id', 'description')
    search_fields = ('description', 'note')
    list_editable = ('is_published',)
    save_on_top = True

    def gethtmlPhoto(self, picture):
        if picture.image:
            return mark_safe(f"<img src='{picture.image.url}' width=50>")

    gethtmlPhoto.short_description = 'миниатюра'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


@admin.register(Commercial)
class CommercialAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    search_fields = ('title',)
    save_on_top = True


class GalleryComercialAdmin(admin.TabularInline):
    model = GalleryComercial
    fields = ('com_image', 'gethtmlPhoto', 'note', 'is_published')
    readonly_fields = ('gethtmlPhoto',)

    def gethtmlPhoto(self, picture):
        if picture.com_image:
            return mark_safe(f"<img src='{picture.com_image.url}' width=75>")

    gethtmlPhoto.short_description = 'миниатюра'


class CommercialObjectAdmin(admin.ModelAdmin):
    inlines = [GalleryComercialAdmin]
    list_display = ('title', 'estate_agent', 'gethtmlPhoto', 'city_region', 'price', 'post_link', 'is_published')
    list_display_links = ('title',)
    search_fields = ('title', 'city_region', 'post_link')
    list_editable = ('is_published',)
    list_filter = ('is_published', 'time_create', 'post_link')
    save_on_top = True

    def gethtmlPhoto(self, picture):
        if picture.image:
            return mark_safe(f"<img src='{picture.image.url}' width=50>")

    gethtmlPhoto.short_description = 'миниатюра'


admin.site.register(InCityObject, InCityObjectAdmin)
admin.site.register(OutCityObject, OutCityObjectAdmin)
admin.site.register(CommercialObject, CommercialObjectAdmin)

admin.site.site_header = 'ЕЦН'
