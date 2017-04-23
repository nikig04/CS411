from django_cron import CronJobBase, Schedule
from FoodAPI.models import Weather

class delete_weather_objects(CronJobBase):
    RUN_EVERY_MINS = 2 # every 24 hours

    schedule = Schedule(run_every_mins=RUN_EVERY_MINS)
    code = 'cron.delete_weather_objects'    # a unique code

    def do(self):
        Weather.objects.all().delete()