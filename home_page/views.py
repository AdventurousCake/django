from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse
import datetime
import requests


def index(request):
    req = requests.get("http://api1.testig.ml/ping")
    if req.status_code != 200:
        raise ConnectionError(f"Status code: {req.status_code}")

    data = {'date': str(datetime.datetime.now()),
            'bot': req.text,
            }
    return render(request, 'home/index.html', data)
    # return HttpResponse("hi")

# def index(request):
#     template = loader.get_template('main/index.html')
#     return HttpResponse(template.render(template, request))

# from django.http import HttpResponse
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")