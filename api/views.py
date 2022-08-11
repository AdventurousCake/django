from rest_framework import permissions
from rest_framework.decorators import api_view, throttle_classes
from rest_framework.response import Response
from rest_framework.throttling import UserRateThrottle
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from api.serializers import MsgSerializer
from home_page.models import Message


@api_view(['GET', 'POST'])
@throttle_classes([UserRateThrottle])
def hello(request):
    if request.method == 'POST':
        return Response({'message': f'Привет {request.data}'})
    return Response({'message': 'Привет, мир!'})


# viewset - multiple actions
class MessagesViewSet(ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MsgSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    # throttle_classes = [UserRateThrottle]
    throttle_scope = 'low_request'


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
