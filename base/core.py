from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login


def get_ivan():
    try:
        user = User.objects.filter(email='ivan.kirigin@gmail.com')[0]
    except:
        user = User.objects.create_user('ivan.kirigin@gmail.com', 'ivan.kirigin@gmail.com', IVAN_PASSWORD)
        user.save()
    return user


def login_ivan(request):
    user = get_ivan()
    user = authenticate(username='ivan.kirigin@gmail.com', password=IVAN_PASSWORD)
    login(request, user)
    return user


def get_token(user=None):
    return 123456