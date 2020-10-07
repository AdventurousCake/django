from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse


def index(request):
    # return HttpResponse("hi")
    return render(request, 'main/hi.html', {})

# def index(request):
#     template = loader.get_template('main/index.html')
#     return HttpResponse(template.render(template, request))

# from django.http import HttpResponse
# def index(request):
#     return HttpResponse("Hello, world. You're at the polls index.")