import datetime

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from base.core import get_ivan, login_ivan, get_token
from base.models import Meal

IVAN_PASSWORD = 'fuckfuck'


    

def home(request):
    s = '<h1>meals:</h2><br/>' + '<br/>'.join([str(meal) for meal in Meal.objects.all()])
    s += '<br/>' + '<br/>'.join(['<a href="%s">%s</a>' % (s,s) for s in get_today_meal_links()])
    return HttpResponse(s)
    

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
