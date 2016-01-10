import datetime
from collections import defaultdict

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.shortcuts import render_to_response 

from base.core import get_ivan, login_ivan, get_token
from base.models import Meal

IVAN_PASSWORD = 'fuckfuck'

def cal(request):
    user = get_ivan()
    meals_by_day, weeks, debug = get_meal_weeks(user)
    return render_to_response('cal.html', {'weeks':weeks, 'meals_by_day':meals_by_day, 'debug':debug})
    

def home(request):
    return cal(request)


def get_meal_weeks(user):
    # get all the meals
    # each day stores a list of meals
    meals_by_day = defaultdict(dict)
    for m in  Meal.objects.filter(user=user):
        meals_by_day[m.date][m.meal_time] = {
            'date': m.date,
            'meal_time': m.meal_time,
            'meal': m,
            'set_good_url': get_meal_set_url(m.date, m.meal_time, True),
            'set_bad_url': get_meal_set_url(m.date, m.meal_time, False),
        }
    # get each day in the week
    dates = meals_by_day.keys()
    earliest = min(dates)
    earliest = earliest - datetime.timedelta(days=earliest.weekday())
    now = datetime.datetime.now()
    d_now = datetime.date(year=now.year, month=now.month, day=now.day)
    d = earliest
    oneday = datetime.timedelta(days=1)
    all_dates = []
    while d < d_now:
        all_dates.append(d)
        d += oneday
    # pick out all the week-starts, make a week list
    starts = filter(lambda d: d.weekday()==0, all_dates)
    starts.sort()
    debug = starts
    # fill up weeks
    weeks = []
    for s in starts:
        week = []
        for td in range(7):
            d = s + datetime.timedelta(days=td)
            day = []
            for meal_time in ['B', 'L', 'D']:
                try:
                    meals_by_day[d][meal_time]
                except:
                    # fill in days that are empty
                    meals_by_day[d][meal_time] = {
                        'date': d,
                        'meal_time': meal_time,
                        'meal': None,
                        'set_good_url': get_meal_set_url(d, meal_time, True),
                        'set_bad_url': get_meal_set_url(d, meal_time, False),
                    }
                day.append(meals_by_day[d][meal_time])
            week.append(day)
        weeks.append(week)
    weeks = weeks[::-1]
    return meals_by_day, weeks, debug


def get_today_meal_links():
    d = datetime.date.today()
    year = d.year
    month = d.month
    day = d.day
    token = get_token()
    urls = []
    for meal in ['B', 'L', 'D']:
        for quality in ['True', 'False']:
            u = "/token_set_meal/%.6d/%.4d/%.2d/%.2d/%s/%s/" % (token, year, month, day, meal, quality)
            urls.append(u)
    return urls


def get_meal_set_url(d, meal_time, quality):
    # should ask for user to get token
    year = d.year
    month = d.month
    day = d.day
    token = get_token()
    q = {True:'True', False:'False'}[quality]
    u = "/token_set_meal/%.6d/%.4d/%.2d/%.2d/%s/%s/" % (token, year, month, day, meal_time, q)
    return u


def go_home():
    return HttpResponseRedirect(reverse('home'))


def token_set_meal(request, token, year, month, day, meal, quality):
    # TODO actually check the token. For now, just get ivan.
    user = login_ivan(request)
    m = update_user_meal(user, year, month, day, meal, quality)
    return go_home()


def set_meal(request, year, month, day, meal, quality):
    user = request.user
    if not request.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    m = update_user_meal(user, year, month, day, meal, quality)
    return go_home()


def update_user_meal(user, year, month, day, meal, quality):
    m = Meal.create_or_update(user, year, month, day, meal, quality)
    return m
