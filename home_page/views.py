from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime
import requests


def index(request):
    date_now = str(datetime.datetime.now().isoformat(' ', 'seconds'))
    data = {'date': date_now,
            'bot': ping(),
            }
    return render(request, 'home/index.html', data)
    # return HttpResponse("hi")


@login_required
def ping():
    req = requests.get("http://api1.testig.ml/ping")
    if req.status_code != 200:
        raise ConnectionError(f"Status code: {req.status_code}")
    return req.json()['status'], " "+str(datetime.datetime.now().isoformat(' ', 'seconds'))


def ping_req(request):
    return HttpResponse(ping())


def bot_users():
    req = requests.get("http://api1.testig.ml/ping")
    if req.status_code != 200:
        raise ConnectionError(f"Status code: {req.status_code}")
    data = req.json()


# def index(request):
#     template = loader.get_template('main/index.html')
#     return HttpResponse(template.render(template, request))

# from django.http import HttpResponse
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
