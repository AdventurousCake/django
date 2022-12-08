from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
import django.http
# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# from django.template import loader
from django.http import Http404, HttpResponse
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView, DetailView, ListView, UpdateView

import logging

from core.models import User
from .forms import MsgForm, CreationFormUser
from .models import Message

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class UserDetails(DetailView):
    # model = User
    template_name = 'form_msg/USERPAGE.html'
    # context_object_name = ''
    # extra_context = 'доп данные'

    # change to context
    queryset = User.objects.all().select_related()

    def get_context_data(self, **kwargs):
        pk = self.kwargs.get('pk', '')

        # v1
        # Call the base implementation first to get a context
        # context = super().get_context_data(**kwargs)
        # context['msgs_data'] = Message.objects.select_related('author').values('id', 'author__username', 'text',
        #                                                                        'created_date') \
        #     .order_by('-created_date') \
        #     .filter(author__id=pk)
        # # .filter(author=self.request.user)
        # return context
        # and in template Записей: {{user.messages.count}}

        # v2
        context = super().get_context_data(**kwargs)
        query = Message.objects.select_related('author').values('id', 'author__username', 'text', 'created_date') \
            .order_by('-created_date') \
            .filter(author__id=pk)

        context['msgs_data'] = query
        context['msgs_data_count'] = query.count()
        return context

    # def get_queryset(self):
    #     pass


# alternative for send_msg
# class MsgFormView(LoginRequiredMixin, CreateView):
#     form_class = MsgForm
#     success_url = reverse_lazy('form_msg:index')
#     template_name = "form_msg/msg_send.html"

class SignUp(CreateView):
    form_class = CreationFormUser
    # success_url = reverse_lazy("form_msg:msg_list")
    success_url = reverse_lazy("login")
    template_name = "form_msg/signup.html"


class MsgList(ListView):
    template_name = "form_msg/msg_list.html"
    paginate_by = 2

    queryset = Message.objects.select_related('author').order_by('-created_date').values('id', 'author__username', 'text',
                                                                'created_date')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MsgList, self).get_context_data(**kwargs)
        return context

# @login_required()
def msg_list(request):
    title = "Messages"
    btn_caption = ""
    template = "form_msg/msg_list.html"

    msgs_data = Message.objects.select_related('author').values('id', 'author__username', 'text',
                                                                'created_date').order_by('-created_date')

    paginator = Paginator(msgs_data, 2)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    # "msgs_data": page
    return render(request, template_name=template,
                  context={"title": title, "object_list": page_obj.object_list, "page_obj": page_obj})


class DetailMsgView(DetailView):
    model = Message

    def get_context_data(self, **kwargs):
        pass


# @login_required()
def get_msg(request, pk):
    # CHECK
    # if request.user.username != username:
    #     return redirect(f"/{username}/{post_id}")

    template = 'form_msg/msg_BY_ID.html'

    # msg = get_object_or_404(klass=Message.objects.select_related("author"), id=pk)
    # show_buttons = msg.author == request.user


    msg = get_object_or_404(klass=Message.objects.select_related("author")
                            .values('id', 'author__username', 'text', 'created_date'),
                            id=pk)

    show_buttons = msg['author__username'] == request.user.username
    is_get_msg = True

    # print(msg.__dict__)

    title = f"Message"
    # title = f"Message #{msg.id}" # query doesnt load
    return render(request, template_name=template,
                  context={"title": title, "msgs_data": msg, "show_buttons": show_buttons, 'is_get_msg': is_get_msg})


class UpdateMsgView(UpdateView):
    model = Message
    form_class = MsgForm

    template_name = "form_msg/msg_send.html"
    success_url = reverse_lazy('form_msg:send_msg')

    def get_object(self, *args, **kwargs):
        obj = super(UpdateMsgView, self).get_object(*args, **kwargs)
        if obj.author != self.request.user:
            raise PermissionDenied()  # or Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "📨 Send message form"
        context['btn_caption'] = "Send"
        context['table_data'] = Message.objects.select_related().order_by('-created_date')[:5]

        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        return super(UpdateMsgView, self).form_valid(form)


@login_required()
def edit_msg(request, pk):
    msg = get_object_or_404(klass=Message, id=pk)
    if msg.author != request.user:
        raise PermissionDenied()
        # return django.http.HttpResponseForbidden()

    title = 'Edit msg'
    template = "form_msg/msg_send.html"
    btn_caption = "Save"
    error = ''

    form = MsgForm(request.POST or None, files=request.FILES or None,
                   instance=msg)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("form_msg:send_msg")
    else:
        error = f'Incorrect form\n' \
                f'{form.errors}'

    return render(request, template_name=template,
                  context={"form": form, "title": title, "btn_caption": btn_caption, "error": error, "data": ""})


@login_required()
def delete_msg(request, pk):
    msg = get_object_or_404(klass=Message, id=pk)
    if msg.author != request.user:
        raise PermissionDenied()

    msg.delete()

    return redirect('form_msg:send_msg')


class MsgFormView(LoginRequiredMixin, CreateView):
    form_class = MsgForm
    template_name = "form_msg/msg_send.html"
    initial = {'text': 'example'}
    success_url = reverse_lazy('form_msg:send_msg')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "📨 Send message form"
        context['btn_caption'] = "Send"
        context['table_data'] = Message.objects.select_related().order_by('-created_date')[:5]

        return context

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.author = self.request.user

        return super(MsgFormView, self).form_valid(form)

    # def form_invalid(self, form):
    #     error
    #     return super(MsgFormView, self).form_invalid(form)


@login_required()
def send_msg(request):
    title = "📨 Send message form"
    btn_caption = "Send"
    template = "form_msg/msg_send.html"

    error = ''
    form = None

    # не оптимально, на каждую связанную таблицу будет запрос (author.id...); если будет цикл - то по каждому айтему еще запрос
    # data = Message.objects.all().order_by('-created_date')[:5]

    # FOR TABLE
    table_data = Message.objects.select_related().order_by('-created_date')[:5]  # INNER JOIN сразу

    form = MsgForm(request.POST or None, request.FILES or None,
                   initial={'text': 'example'})  # and FILES

    if form.is_valid() and request.method == "POST":
        msg = form.save(commit=False)
        msg.author = request.user
        msg.save()

        # fields actions
        # cd = form.cleaned_data
        # form.save()
        # form.save(commit=True)

        # # Создаем комментарий, но пока не сохраняем в базе данных.
        # new_comment = comment_form.save(commit=False)
        # # Привязываем комментарий к текущей статье.
        # new_comment.post = post
        # # Сохраняем комментарий в базе данных.
        # new_comment.save()

        # or render in end
        # for msg table on page
        return redirect('form_msg:send_msg')
    else:
        # сброс формы с данными
        # old_form_with_errors = form
        # form = MsgForm()

        error = f'Incorrect form\n' \
                f'{form.errors}'
        # return render(request, "form_msg/msg_send.html", {"form": form, "title": title, "btn_caption": btn_caption, "error": error})

    return render(request, template_name=template, context=
    {"form": form, "title": title, "btn_caption": btn_caption, "error": error, "table_data": table_data})
