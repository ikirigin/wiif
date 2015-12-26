from django.db import models
from django.contrib.auth.models import User
import datetime

"""
What to do here?

first we need to make sure we can save any data at all. 

We should push local dev data into the same configuration as prod -- a heroku box


But then we need to model what data we're going to record here.

If we had a model for the food being recorded 


"""
DATE_FORMAT = '%Y-%m-%d'

def date_strptime(s):
    dt = datetime.datetime.strptime(s, DATE_FORMAT)
    d = datetime.date(dt.year, dt.monht, dt.day)
    return d


class Meal(models.Model):
    MEAL_TIMES = (
        ('B', 'breakfast'),
        ('L', 'lunch'),
        ('D', 'dinner'),
    )
    user = models.ForeignKey(User, db_index=True)
    date = models.DateField(db_index=True, null=True)
    # which meal
    meal_time = models.CharField(max_length=1, choices=MEAL_TIMES)
    # True=good, False=bad
    quality = models.BooleanField(default=False)
    prompt_sent = models.BooleanField(default=False) 
    
    @classmethod
    def create_or_update(cls, user, year, month, day, meal, quality):
        if meal not in ['B', 'L', 'D']:
            return None
        d = datetime.date(year=int(year), month=int(month), day=int(day))
        quality = {'False':False, 'True':True}[quality]
        try:
            m = Meal.objects.filter(user=user, date=d, meal_time=meal)[0]
            m.quality = quality
        except:
            m = Meal(user=user, date=d, meal_time=meal, quality=quality)
        m.save()
        return m

    
    def __str__(self):
        return self.date.strftime(DATE_FORMAT) + ' ' + self.meal_time + ': ' + str(self.quality)


'''
class Caffeine(models.Model):
    day
    user
    count

class Alcohol(models.Model):
    day
    user
    count
'''