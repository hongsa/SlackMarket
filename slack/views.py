from slack.models import Slack,User,Register
from slack.serializers import SlackSerializer,UserSerializer,RegisterSerializer
from rest_framework import generics
from rest_framework import permissions
import logging
logger = logging.getLogger(__name__)


class SlackList(generics.ListCreateAPIView):
    queryset = Slack.objects.all()
    serializer_class = SlackSerializer
    #User외래키 값 입력을 위한 오버라이딩 메소드
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SlackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Slack.objects.all()
    serializer_class = SlackSerializer


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterList(generics.ListCreateAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer

    #user, slack 외래키 값 입력을 위한 오버라이딩 메소드
    def perform_create(self, serializer):
        # requeset.POST or request.data ??
        queryset = Slack.objects.get(self.request.POST.get('slack'))
        serializer.save(user=self.request.user,slack=queryset)
