import logging

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView

from core.models import User
from .forms import MsgForm, CreationFormUser, CommentForm
from .models import Message, Comment

# from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)


class UserDetails(DetailView):
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


class SignUp(CreateView):
    form_class = CreationFormUser
    success_url = reverse_lazy("login")  # reverse_lazy("form_msg:msg_list")
    template_name = "form_msg/signup.html"


class MsgList(ListView):
    """List of messages with user likes"""
    template_name = "form_msg/msg_list.html"

    paginate_by = 2

    # queryset = Message.objects.select_related('author') \
    #     .values('id', 'author__username', 'text', 'created_date') \
    #     .order_by('-created_date')

    # [:3]
    queryset = Message.objects.select_related('author').prefetch_related('likes')

    # queryset = Message.objects.select_related('author').prefetch_related('likes') \
    #     .values('id', 'author__username', 'text', 'created_date', 'likes__user',) \
    #     .order_by('-created_date')

    # TODO move to get_queryset?
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(MsgList, self).get_context_data(**kwargs)

        # msg ids which user likes
        if self.request.user.is_authenticated:
            msgs = self.queryset  # fix pagination
            # msgs = context['object_list']

            context['show_buttons'] = True
            # likes_count in template

            # not used DEBUG
            # msgs2=msgs.values('id').annotate(likes_cnt=Count('likes__id')).order_by('id')

            # OLD
            # msgs2 = Message.objects.annotate(
            #     like_id=F('likes__id'),
            #     likes_cnt=Count('likes__id')
            # ).values('id', 'likes_cnt').order_by('id')
            #
            # msgs2 = msgs.all().values('id', 'likes__user', count=Count('likes'))
            # for id, data_list in groupby(msgs2, lambda x: x.get('id')):
            #     print(f"msg id {id} : {list(data_list)}")

            # user likes msg ids
            context['user_likes'] = msgs.filter(likes__user=self.request.user.id).values_list('id', flat=True)
            print(context['user_likes'])
        return context

        # # msg ids which user likes
        # if self.request.user.is_authenticated:
        #     context['likes'] = Like.objects.filter(message__in=context['object_list'].values_list('id', flat=True),
        #                                            user=self.request.user) \
        #         .values_list('message__id', flat=True)
        #     print(context['likes'])
        # return context


class DetailMsgView(DetailView):
    model = Message
    template_name = 'form_msg/msg_BY_ID.html'
    context_object_name = 'msg'

    # queryset = Message.objects.select_related("author", "comments").values('id', 'author__username', 'text',
    #                                                                        'created_date')

    # values('id', 'author__username', 'text', 'created_date', 'comments__id','comments__user', 'comments__text')

    def get_queryset(self):
        return get_object_or_404(klass=Message.objects.select_related("author", "comments")
                                 .values('id', 'author__username', 'text', 'created_date'),
                                 id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Message'
        context['is_detail_msg'] = True
        context['show_edit_buttons'] = self.object.get('author__username') == self.request.user.username
        context['comments'] = Comment.objects.filter(message_id=self.object.get('id'))
        return context


class DetailMsgANDCommentView(CreateView):
    model = Message
    template_name = 'form_msg/msg_BY_ID.html'
    context_object_name = 'msg'
    form_class = CommentForm

    queryset = Message.objects.select_related("author", "comments").values('id', 'author__username', 'text',
                                                                           'created_date')  # may save form issue

    def get_success_url(self):
        return reverse_lazy('form_msg:show_msg', kwargs={'pk': self.kwargs['pk']})

    # def get_object(self, queryset=None):
    #     pk = self.kwargs['pk']
    #     return get_object_or_404(
    #         klass=Message.objects.select_related("author", "comments").values('id', 'author__username', 'text',
    #                                                                           'created_date'), pk=pk)

    # .values('id', 'author__username', 'text', 'created_date', 'comments__id','comments__user', 'comments__text')

    # def get_queryset(self):
    #     return get_object_or_404(klass=Message.objects.select_related("author")
    #                              .values('id', 'author__username', 'text', 'created_date'),
    #                              id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        msg = self.get_object()
        context = super().get_context_data(**kwargs)
        context['title'] = 'Message'
        context['is_detail_msg'] = True
        context['show_edit_buttons'] = msg.get('author__username') == self.request.user.username

        # context['comments'] = Comment.objects.filter(message__id=self.object.get('id')) # none err get
        context['comments'] = Comment.objects.select_related('user').filter(message__id=msg.get('id')).values(
            'user__username', 'text')
        context['msg'] = msg
        return context

    def form_valid(self, form):
        if self.request.user.is_anonymous:
            raise PermissionDenied()

        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.message = Message.objects.get(pk=self.kwargs['pk'])
        # obj.message = self.get_object()

        return super(DetailMsgANDCommentView, self).form_valid(form)


class UpdateMsgView(LoginRequiredMixin, UpdateView):
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


class DeleteMsgView(LoginRequiredMixin, DeleteView):
    model = Message
    success_url = reverse_lazy('form_msg:send_msg')

    # ignore confirm template
    def get(self, request, *args, **kwargs):
        # return self.post(request, *args, **kwargs)
        return self.delete(request, *args, **kwargs)

    def get_object(self, *args, **kwargs):
        obj = super(DeleteMsgView, self).get_object(*args, **kwargs)
        if obj.author != self.request.user:
            raise PermissionDenied()  # or Http404
        return obj


class MsgFormCreateView(LoginRequiredMixin, CreateView):
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

        return super(MsgFormCreateView, self).form_valid(form)

    # def form_invalid(self, form):
    #     error
    #     return super(MsgFormCreateView, self).form_invalid(form)
