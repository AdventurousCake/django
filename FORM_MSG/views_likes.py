from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import UpdateView
from django.views.generic.edit import BaseUpdateView

from FORM_MSG.models import Like, Message


# get in api or viewlist

# def post(request):
# message_id = request.POST.get('message_id')
# liked = request.POST.get('liked')

# Check if the user has already liked the message
#         if liked == 'true':
#             # The user has already liked the message, so remove the like
#             Like.objects.filter(user=user, message=message).delete()
#             return JsonResponse({'liked': False})
#         else:
#             # The user has not liked the message, so add a like
#             Like.objects.create(user=user, message=message)
#             return JsonResponse({'liked': True})


class UpdateLikeView(LoginRequiredMixin, BaseUpdateView):
    model = Like
    fields = ('likes',)

    def get_object(self, queryset=None):
        return get_object_or_404(klass=Message, id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        obj: Message = self.get_object()

        # todo if liked == 'true':
        # action = self.kwargs['pk']

        if not obj.likes.filter(user=self.request.user, message=obj).exists():
            # only check oem query
            try:
                obj.likes.create(user=self.request.user, message=obj)
                obj.save()
            except IntegrityError:
                return JsonResponse({'status': 'error'})

            # return JsonResponse({'status': 'ok',
            #                      'like_count': obj.likes.count()})

        else:
            obj.likes.filter(user=self.request.user, message=obj).delete()
            # return JsonResponse({'status': 'ok',
            #                      'like_count': obj.likes.count()})

        return redirect(to=reverse('form_msg:msg_list'))
