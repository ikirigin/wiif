import datetime
from django.core.management.base import BaseCommand, CommandError

from base.core import get_ivan, get_token, send_email, get_meal_params
from base.models import Meal, WifeNotified

class Command(BaseCommand):
    help = "Tell Abby about the bad meal"
    
    def handle(self, *args, **options):
        ivan = get_ivan()
        # check the current meal
        now = datetime.datetime.now()
        d, meal_time = get_meal_params(now)
        
        try:
            m = Meal.objects.filter(user=ivan).filter(date=d).filter(meal_time=meal_time)[0]
        except:
            print 'bad_meal_notif: no meal found at ', now
            # empty DB
            return
        
        # if it was fine, don't notify
        if m.quality:
            return
        
        # if it was bad, check if there was a notification already
        try:
            w = WifeNotified.objects.filter(user=ivan, meal=m)[0]
            return
        except:
            # create the record
            w = WifeNotified(user=ivan, meal=m)
            w.save()
        
        # now send the notification
        meal = {'B':'breakfast', 'L':'lunch', 'D':'dinner'}[m.meal_time]
        day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][m.date.weekday()]
        subject = "Ivan had a bad %s on %s, %0.4d/%d/%d" % (meal, day_of_week, m.date.year, m.date.month, m.date.day)
        text = "what did you eat?"
        to=["abigail.kirigin@gmail.com", "ivan.kirigin@gmail.com"]
        send_email(to, subject, text, text)