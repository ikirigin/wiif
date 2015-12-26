from django.core.management.base import BaseCommand, CommandError

from base.core import get_ivan, get_token, send_email
from base.models import Meal, WifeNotified

class Command(BaseCommand):
    help = "Tell Abby about the bad meal"
    
    def handle(self, *args, **options):
        pass
        # check the last meal
        try:
            m = Meal.objects.filter(user=get_ivan()).order_by("-created_at")[0]
        except:
            # empty DB
            return
        # if it was fine, don't notify
        if m.quality:
            return
        # if it was bad, check if there was a notification already
        try:
            q = MealQueried.objects.filter(user=ivan, date=today, meal_time=meal_time)[0]
            return
        except:
            # create the record
            q = MealQueried(user=ivan, date=today, meal_time=meal_time)
            q.save()
        
        # now send the notification
        
        meal = {'B':'breakfast', 'L':'lunch', 'D':'dinner'}[m.meal_time]
        day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][m.date.weekday()]
        subject = "Ivan had a bad %s on %s, %0.4d/%d/%d" % (meal, day_of_week, m.date.year, m.date.month, m.date.day)
        text = "what did you eat?"
        
        send_email(to=["abigail.kirigin@gmail.com", "ivan.kirigin@gmail.com"], subject, text, text)