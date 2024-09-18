from django.core.management.base import BaseCommand
from ecn.models import *
from ecn.slugify import words_to_slug
from random import choice
import random


class Command(BaseCommand):
    help = 'Displays current time'

    def handle(self, *args, **kwargs):
        object_types = InCityObjectType.objects.all()
        weights = [2, 5, 2, 1]
        object_type = random.choices(object_types, weights)[0]
        print(object_type)

        
