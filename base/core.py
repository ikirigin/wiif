import requests
import datetime

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from wiif.settings import MAILGUN_URL, MAILGUN_API_KEY, MAILGUN_FROM


def get_meal_params(t):
    """ given a date time, find the current meal and date
    """
    if t.hour < 12:
        meal_time = 'B'
    elif t.hour < 17:
        meal_time = 'L'
    elif t.hour < 19:
        meal_time = 'D'
    d = datetime.date(year=t.year, month=t.month, day=t.day)
    return (d, meal_time)


def send_email(to, subject, text, html=None):
    data = {
        "from": MAILGUN_FROM,
        "to": to,
        "subject": subject,
        "text": text,
        'html': html,
    }
    r = requests.post(MAILGUN_URL + '/messages', auth=("api", MAILGUN_API_KEY), data=data)


def get_ivan():
    try:
        user = User.objects.filter(email='ivan.kirigin@gmail.com')[0]
    except:
        user = User.objects.create_user('ivan.kirigin@gmail.com', 'ivan.kirigin@gmail.com', 'fuckfuck')
        user.save()
    return user


def login_ivan(request):
    user = get_ivan()
    user = authenticate(username='ivan.kirigin@gmail.com', password='fuckfuck')
    login(request, user)
    return user


def get_token(user=None):
    return 123456