import datetime
from collections import defaultdict

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response 
from django.template import RequestContext

from base.core import get_token
from base.models import Meal

IVAN_PASSWORD = 'fuckfuck'

def cal(request):
    user = request.user
    meals_by_day, weeks = get_meal_weeks(user)
    return render_to_response('cal.html', {'weeks':weeks, 'meals_by_day':meals_by_day, 'user':user})
    

def landing(request):
    return render_to_response('landing.html', {}, context_instance=RequestContext(request))


def home(request):
    if request.user.is_authenticated():
        return cal(request)
    else:
        return landing(request)
        


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
    if not dates:
        dates = [datetime.date.today()]
    earliest = min(dates)
    earliest = earliest - datetime.timedelta(days=earliest.weekday())
    now = datetime.datetime.now()
    d_now = datetime.date(year=now.year, month=now.month, day=now.day)
    d = earliest
    oneday = datetime.timedelta(days=1)
    all_dates = []
    while d <= d_now:
        all_dates.append(d)
        d += oneday
    # pick out all the week-starts, make a week list
    starts = filter(lambda d: d.weekday()==0, all_dates)
    starts.sort()
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
    return meals_by_day, weeks


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
    user = request.user
    if not request.user.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    m = update_user_meal(user, year, month, day, meal, quality)
    return go_home()


def set_meal(request, year, month, day, meal, quality):
    user = request.user
    if not request.is_authenticated():
        return HttpResponseRedirect(reverse('login'))
    m = update_user_meal(user, year, month, day, meal, quality)
    return go_home()


def update_user_meal(user, year, month, day, meal, quality):
    m = Meal.create_or_update(user, year, month, day, meal, quality)
    return m


def login_user(request):
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'GET':
        context = RequestContext({})
        return render_to_response('login.html', {}, context_instance=RequestContext(request))
    elif request.method != 'POST':
        return HttpResponseRedirect(reverse('home'))
    email = request.POST.get('email','')
    password = request.POST.get('password','')
    if not email or not password:
        return HttpResponseRedirect(reverse('login')+'?missing_email_or_password')
    user = authenticate(username=email, password=password)
    if user:
        login(request, user)
        return HttpResponseRedirect(reverse('home'))
    else:
        return HttpResponseRedirect(reverse('login')+'?bad_login')


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('home')+'?loggedout')


def signup_user(request):
    user = request.user
    if user.is_authenticated():
        return HttpResponseRedirect(reverse('home'))
    if request.method == 'GET':
        context = RequestContext({})
        return render_to_response('signup.html', {}, context_instance=RequestContext(request))
    elif request.method != 'POST':
        return HttpResponseRedirect(reverse('home'))
    email = request.POST.get('email','')
    password = request.POST.get('password','')
    if not email or not password:
        return HttpResponseRedirect(reverse('signup')+'?missing_email_or_password')
    user = User.objects.create_user(email, email, password)
    user = authenticate(username=email, password=password)
    login(request, user)
    return HttpResponseRedirect(reverse('home'))