from django import template

from ecn.models import *

register = template.Library()


@register.inclusion_tag('ecn/inclusion/header.html')
def show_header(user='user'):
    logo = Graphics.objects.get(description='логотип')
    in_city_object_type = InCityObjectType.objects.filter(in_main_page=True)
    out_city_object_type = OutCityObjectType.objects.filter(in_main_page=True)
    return {
        "logo": logo,
        'in_city_object_type': in_city_object_type,
        'out_city_object_type': out_city_object_type,
        'user': user
    }


@register.inclusion_tag('ecn/inclusion/links_list.html')
def links_list(link='rooms'):
    if link == 'obj_type':
        list_links = InCityObjectType.objects.all().values('id', 'title')
        view_name = 'searched_object_type'
        s_o_r = 's'

    elif link == 'regions':
        list_links = InCityRegion.objects.all().values('id', 'title')
        view_name = 'searched_obj_region'
        s_o_r = 's'

    elif link == 'rent_rooms':
        list_links = RoomAmount.objects.all().values('id', 'title')
        view_name = 'searched_obj_rooms'
        s_o_r = 'r'

    elif link == 'rent_regions':
        list_links = InCityRegion.objects.all().values('id', 'title')
        view_name = 'searched_obj_region'
        s_o_r = 'r'
    else:
        list_links = RoomAmount.objects.all().values('id', 'title')
        view_name = 'searched_obj_rooms'
        s_o_r = 's'

    return {
        'view_name': view_name,
        'list_links': list_links,
        'sale_or_rent': s_o_r
    }
