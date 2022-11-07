from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
# from django.template import loader
from django.http import Http404
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView

import datetime
import requests
import logging
import locale

from core.models import User
from home_page.forms import MsgForm, CreationForm
from home_page.models import Message

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class UserDetails(DetailView):
    # model = User
    template_name = 'home/USERPAGE.html'
    # context_object_name = ''
    # extra_context = 'доп данные'

    queryset = User.objects.all().select_related()

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk', '')

        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        # Add in a QuerySet of all the books
        context['msgs_data'] = Message.objects.select_related('author').values('author__username', 'text',
                                                                               'created_date') \
            .order_by('-created_date') \
            .filter(author__id=pk)  # !! todo filter; count
        # .filter(author=self.request.user) # !! todo filter; count
        return context

    # def get_queryset(self):
    #     pass


# alternative for send_msg
# class MsgFormView(LoginRequiredMixin, CreateView):
#     form_class = MsgForm
#     success_url = reverse_lazy('home:index')
#     template_name = "home/msg_send.html"

class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("home:index")
    # success_url = reverse_lazy("login")  # где login — это параметр "name" в path()
    template_name = "home/signup.html"


@login_required()
def msg_list(request):
    title = "Messages"
    btn_caption = ""
    template = "home/msg_list.html"

    msgs_data = Message.objects.select_related('author').values('author__username', 'text', 'created_date').order_by(
        '-created_date')

    return render(request, template_name=template, context={"title": title, "msgs_data": msgs_data})


@login_required()
def get_msg(request, pk):
    # CHECK
    # if request.user.username != username:
    #     return redirect(f"/{username}/{post_id}")

    template = 'home/msg_BY_ID.html'
    msg = get_object_or_404(klass=Message, id=pk)

    # print(msg.__dict__)

    title = f"Message"
    # title = f"Message #{msg.id}" # query doesnt load
    return render(request, template_name=template, context={"title": title, "msgs_data": msg})


@login_required()
def edit_msg(request, pk):
    # msg = Message.objects.get(pk)

    # TODO PK SECURITY; check author
    msg = get_object_or_404(klass=Message, id=pk)
    title = 'Edit msg'
    template = "home/msg_send.html"
    btn_caption = "Save"
    error = ''

    form = MsgForm(request.POST or None, files=request.FILES or None, instance=msg)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("home:send_msg")
    else:
        error = f'Incorrect form\n' \
                f'{form.errors}'

    return render(request, template_name=template, context=
    {"form": form, "title": title, "btn_caption": btn_caption, "error": error, "data": ""})


@login_required()
def delete_msg(request, pk):
    # CHECK
    # if request.user.username != username:
    #     return redirect(f"/{username}/{post_id}")

    msg = get_object_or_404(klass=Message, id=pk)
    msg.delete()

    return redirect('home:send_msg')


@login_required()
def send_msg(request):
    title = "📨 Send message form"
    btn_caption = "Send"
    template = "home/msg_send.html"

    error = ''
    form = None

    # не оптимально, на каждую связанную таблицу будет запрос (author.id...); если будет цикл - то по каждому айтему еще запрос
    # data = Message.objects.all().order_by('-created_date')[:5]

    # INNER JOIN сразу
    msgs_data = Message.objects.select_related().order_by('-created_date')[:5]

    form = MsgForm(request.POST or None, request.FILES or None,
                   initial={'text': 'example'})  # and FILES
    # form = MsgForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        # if form.is_valid():
        form.save(commit=True)

        # fields actions
        # cd = form.cleaned_data
        # form.save()

        # # Создаем комментарий, но пока не сохраняем в базе данных.
        # new_comment = comment_form.save(commit=False)
        # # Привязываем комментарий к текущей статье.
        # new_comment.post = post
        # # Сохраняем комментарий в базе данных.
        # new_comment.save()

        # or render in end
        # return redirect('home:index')
        return redirect('home:send_msg')
    else:
        # сброс формы с данными
        # old_form_with_errors = form
        # form = MsgForm()

        error = f'Incorrect form\n' \
                f'{form.errors}'
        # return render(request, "home/msg_send.html", {"form": form, "title": title, "btn_caption": btn_caption, "error": error})

    return render(request, template_name=template, context=
    {"form": form, "title": title, "btn_caption": btn_caption, "error": error, "data": msgs_data})


# @login_required
def index_page(request):
    date_now = str(datetime.datetime.now().isoformat(' ', 'seconds'))
    data = {'date': date_now,
            'bot': _ping(),
            'userinfo': {
                'username': request.user.username,
                'is_staff': request.user.is_staff
            },
            'date_block': get_date_format()
            }
    return render(request, 'home/index.html', data)
    # return HttpResponse("hi")


def get_date_format():
    # with locale.setlocale(locale.LC_ALL, 'ru_RU.utf8'):
    result = datetime.datetime.now().strftime("%A, %#d %B") # "📅 " +
    return result


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
