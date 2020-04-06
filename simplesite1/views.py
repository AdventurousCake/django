from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.http import Http404
from django.urls import reverse


# def index(request):
#     template = loader.get_template('simplesite1/index.html')
#     return HttpResponse(template.render(template, request))

def index(request):
    context = {}
    return render(request, 'simplesite1/index.html', context)


# def index(request):
#     return render(request, 'home/index.html')
#
# def index(request):
#     #context = {}
#     return render(request, 'main/index.html')

