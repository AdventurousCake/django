from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from django.template import loader
from django.http import Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
import datetime
import requests
import logging

from home_page.forms import MsgForm

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


@login_required()
def send_msg(request):
    form = MsgForm(request.POST or None)
    if form.is_valid():
        form.save(commit=True)
        # fields actions
        # form.save()
        return redirect('home:index')


def index(request):
    date_now = str(datetime.datetime.now().isoformat(' ', 'seconds'))
    data = {'date': date_now,
            'bot': _ping(),
            }
    return render(request, 'home/index.html', data)
    # return HttpResponse("hi")


def _ping():
    try:
        req = requests.get("https://api1.testig.ml/ping", timeout=1)
    except Exception as e:
        print(e)
        return None

    # req.raise_for_status()
    if req.status_code != 200:
        # raise ConnectionError(f"Status code: {req.status_code}")
        log.error(f"ping bot: Status code: {req.status_code}")
        return f"ping bot: Status code: {req.status_code}"
    return req.json()['status'], " " + str(datetime.datetime.now().isoformat(' ', 'seconds'))


@login_required
def ping_req(request):
    return HttpResponse(_ping())


def _bot_stats():
    # example
    req = requests.get("https://api1.testig.ml/URL")
    if req.status_code != 200:
        log.error(f"stats bot: Status code: {req.status_code}")
        # raise ConnectionError(f"Status code: {req.status_code}")
        return 0
    data = req.json()
    return data


def admin_old_page(request):
    return HttpResponse("<h1>new admin</h1>")

# def index(request):
#     template = loader.get_template('main/index.html')
#     return HttpResponse(template.render(template, request))

# from django.http import HttpResponse
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")
