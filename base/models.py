from django.db import models
from django.contrib.auth.models import User

"""
What to do here?

first we need to make sure we can save any data at all. 

We should push local dev data into the same configuration as prod -- a heroku box


But then we need to model what data we're going to record here.

If we had a model for the food being recorded 


"""


class Meal(models.Model):
    MEAL_TIMES = (
        ('B', 'breakfast'),
        ('L', 'lunch'),
        ('D', 'dinner'),
    )
    user = models.ForeignKey(User)
    created_at = models.DateField()
    # which meal
    meal_time = models.CharField(max_length=1, choices=MEAL_TIMES)
    # True=good, False=bad
    quality = models.BooleanField(default=False)