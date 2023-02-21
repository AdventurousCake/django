from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import IntegrityError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import UpdateView
from django.views.generic.edit import BaseUpdateView
from rest_framework import status, permissions
from rest_framework.generics import GenericAPIView
from rest_framework.mixins import UpdateModelMixin
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet

from FORM_MSG.models import Like, Message
from api.serializers import LikeSerializerSIMPLE, LikeSerializerSIMPLE2

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


# used for form action, then redirect to LIST; uses only django
from core.models import User


# Django
class UpdateLikeView(LoginRequiredMixin, BaseUpdateView):
    model = Like

    # fields = ('likes',) # form

    # def get_object(self, queryset=None):
    #     return get_object_or_404(klass=Message, id=self.kwargs['pk'])

    def post(self, request, *args, **kwargs):
        # using func, not method

        msg: Message = get_object_or_404(klass=Message.objects.only('id'), id=self.kwargs['pk'])
        like, is_created = Like.objects.get_or_create(user=self.request.user, message=msg)  # returns all fields
        if not is_created:
            like.delete()
        return redirect(reverse('form_msg:msg_list'))

    def post_OLD(self, request, *args, **kwargs):
        obj: Message = self.get_object()

        if not obj.likes.filter(user=self.request.user, message=obj).exists():
            # only check orm query
            try:
                obj.likes.create(user=self.request.user, message=obj)
                obj.save()

            # date not null constraint error
            except Exception as e:
                print(e)

            # DoesNotExist processing in getor404

            # except IntegrityError:
            #     return Response({'status': 'error:UpdateLikeView'})
            # return Response({'status': 'ok', 'like_count': obj.likes.count()})

        else:
            obj.likes.filter(user=self.request.user, message=obj).delete()
            # return Response({'status': 'ok', 'like_count': obj.likes.count()})
        return redirect(to=reverse('form_msg:msg_list'))


# API apiview; Anon user fixme
class UpdateLikeViewAPI(APIView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, pk):
        msg = get_object_or_404(Message, id=pk)
        try:
            u = User.objects.get(pk=1)
            like, is_created = Like.objects.get_or_create(user=u, message=msg)
            # like, is_created = Like.objects.get_or_create(user=self.request.user, message=msg)

            if not is_created:
                like.delete()

            # return Response(status=status.HTTP_204_NO_CONTENT)
            return redirect(to=reverse('form_msg:msg_list'))
        except IntegrityError as e:
            return Response({'error': f'Error updating like: {str(e)}'})


# API gengericApiView
class UpdateLikeViewGenericAPIView(UpdateModelMixin, GenericAPIView):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LikeSerializerSIMPLE

    def post(self, request, *args, **kwargs):
        msg = get_object_or_404(Message, id=kwargs['pk'])
        try:
            u = User.objects.get(pk=1)
            like, is_created = Like.objects.get_or_create(user=u, message=msg)
            # like, is_created = Like.objects.get_or_create(user=self.request.user, message=msg)

            if not is_created:
                like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError as e:
            return Response({'error': f'Error updating like: {str(e)}'})


# API mix
class UpdateLikeMix(UpdateModelMixin, GenericViewSet):
    permission_classes = (permissions.AllowAny,)
    serializer_class = LikeSerializerSIMPLE

    # PUT, PATCH; createmix - post
    def update(self, request, *args, **kwargs):
        msg = get_object_or_404(Message, id=kwargs['pk'])
        try:
            u = User.objects.get(pk=1)
            like, is_created = Like.objects.get_or_create(user=u, message=msg)
            # like, is_created = Like.objects.get_or_create(user=self.request.user, message=msg)
            if not is_created:
                like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except IntegrityError as e:
            return Response({'error': f'Error updating like: {str(e)}'})
