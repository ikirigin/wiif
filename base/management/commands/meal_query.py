import datetime

from django.core.management.base import BaseCommand, CommandError

from base.core import get_ivan, get_token

from base.models import Meal

def send_gmail(tos, subject, msg_text, msg_html):
    pass



class Command(BaseCommand):
    help = 'Email Ivan and ask about the last meal'
    
    def handle(self, *args, **options):
        user = get_ivan()
        today = datetime.date.today()
        # check the time for the meal.
        now = datetime.datetime.now()
        if now.house < 10:
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
        
        try:
            m = Meal.objects.filter(user=ivan, date=today, meal_time=meal_time)[0]
            # this meal slot already exists, don't do anything
            return
        except:
            pass
        
        token = get_token()
        year = today.year
        month = today.month
        day = today.day
        
        good_url = "/token_set_meal/%.6d/%.4d/%.2d/%.2d/%s/%s/" % (token, year, month, day, meal_time, 'True')
        bad_url = "/token_set_meal/%.6d/%.4d/%.2d/%.2d/%s/%s/" % (token, year, month, day, meal_time, 'False')
        
        meal = {'B':'breakfast', 'L':'lunch', 'D':'dinner'}[meal_time]
        day_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'][today.weekday()]
        subject = "%s on %s, %.4d/%.2d/%.2d" % (meal, day_of_week, year, month, day)
        body = """<a href="%s">GOOD</a><br/>
<br/>
<a href="%s">BAD</a>
<br/>
your next decision is important
"""