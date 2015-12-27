import datetime
import random
import requests

from django.core.management.base import BaseCommand, CommandError

from base.core import get_ivan, get_token, send_email
from base.models import Meal, MealQueried


class Command(BaseCommand):
    help = 'Email Ivan and ask about the last meal'
    
    def handle(self, *args, **options):
        ivan = get_ivan()
        today = datetime.date.today()
        # check the time for the meal.
        now = datetime.datetime.now()
        if now.hour < 10:
            # don't ask if it is in the morning
            # assume dinner last night was sent 
            return
        elif now.hour < 12:
            meal_time = 'B'
        elif now.hour < 15:
            # don't ask about lunch before 3pm
            return
        elif now.hour < 17:
            meal_time = 'L'
        elif now.hour < 19:
            # don't ask about dinner before 7pm
            return          
        else:
            meal_time = 'D'
        
        # check if the meal exists
        try:
            m = Meal.objects.filter(user=ivan, date=today, meal_time=meal_time)[0]
            return
        except:
            pass
        
        # check if the prompt was already sent
        try:
            q = MealQueried.objects.filter(user=ivan, date=today, meal_time=meal_time)[0]
            return
        except:
            # create the record
            q = MealQueried(user=ivan, date=today, meal_time=meal_time)
            q.save()
        
        token = get_token()
        year = today.year
        month = today.month
        day = today.day
        
        good_url = "http://www.wiifapp.com/token_set_meal/%.6d/%.4d/%.2d/%.2d/%s/%s/" % (token, year, month, day, meal_time, 'True')
        bad_url = "http://www.wiifapp.com/token_set_meal/%.6d/%.4d/%.2d/%.2d/%s/%s/" % (token, year, month, day, meal_time, 'False')
        
        meal = {'B':'breakfast', 'L':'lunch', 'D':'dinner'}[meal_time]
        day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][today.weekday()]
        subject = "%s on %s, %.4d/%.2d/%.2d" % (meal, day_of_week, year, month, day)
        saying = random.choice([
            "just fucking do it",
            "your next decision is important",
            "hang in there!",
            "anyone in the race laps everyone on the couch",
            "be the change you want to see in the world",
            "some people die at 25 and aren't buried till 75",
            "turn down for what",
            "don't start no shit wont be no shit",
        ])
        html = """<a href="%s">GOOD</a><br/>
<br/>
<a href="%s">BAD</a><br/>
<br/>
%s
""" % (good_url, bad_url, saying)
        text = "http://www.wiifapp.com/"
        send_email('ivan.kirigin@gmail.com', subject, text, html)