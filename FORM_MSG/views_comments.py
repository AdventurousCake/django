from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic.edit import BaseUpdateView, BaseCreateView

from FORM_MSG.forms import CommentForm
from FORM_MSG.models import Comment, Message


# UNUSED
class UpdateLikeView(LoginRequiredMixin, BaseCreateView):
    model = Comment
    form_class = CommentForm

    # def get_object(self, queryset=None):
    #     return get_object_or_404(klass=Comment, id=self.kwargs['pk'])

    def get(self, request, *args, **kwargs):

        msg: Message = get_object_or_404(klass=Comment.objects.only('id'), id=self.kwargs['pk'])

        # valid + csrf
        text = self.kwargs['text']
        comment, is_created = Comment.objects.get_or_create(user=self.request.user, message=msg, text=text)

        return redirect(reverse('form_msg:show_msg', kwargs={'pk': self.kwargs['pk']}))
