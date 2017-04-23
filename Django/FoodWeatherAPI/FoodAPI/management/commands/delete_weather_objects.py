from django.core.management.base import BaseCommand
from FoodAPI.models import Weather

class Command(BaseCommand):
    def handle(self, *args, **options):
        Weather.objects.all().delete()