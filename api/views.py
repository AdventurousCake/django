from rest_framework import permissions, filters
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from api.serializers import MsgSerializer, UserSerializer, MsgSerializerSearch
from home_page.models import Message
from core.models import User


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


# alt users ReadOnlyModelViewSet; др юзеры не могут менять данные
class UserViewSetRO(ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer = UserSerializer


# global permissions dep; необходимо каждый раз передавать token, получив через auth
class UserList(APIView):
    def get(self, request, username):
        users = User.objects.filter(username=username)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)


# GET http://127.0.0.1:8000/api/v1/msg_search/?search=123
# GET http://127.0.0.1:8000/api/v1/msg_search/?text=236263
# viewset с фильтром и поиском
class MsgList(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MsgSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['text', ]  # 'name'
    permission_classes = (permissions.IsAuthenticated,)
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    ordering_fields = ['-created_date']


# viewset - multiple actions
class MessagesViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MsgSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # throttle_classes = [UserRateThrottle]
    throttle_scope = 'low_request'

    def perform_create(self, serializer):
        if self.request.user:
            serializer.save(author=self.request.user)
        else:
            print(self.request.user)
            serializer.save(author='unknown')

@api_view(['GET', 'POST'])
@throttle_classes([UserRateThrottle])
def hello(request):
    if request.method == 'POST':
        return Response({'message': f'Привет {request.data}'})
    return Response({'message': 'Привет, мир!'})


class ExampleView(APIView):
    #  здесь подключили класс UserRateThrottle
    #  и для этого view-класса сработает лимит "10000/day" для залогиненных пользователей,
    #  объявленный в settings.py
    throttle_classes = [UserRateThrottle]

    def get(self, request):
        text = {
            'hello': 'world'
        }
        return Response(text)
