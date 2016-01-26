from django.contrib.auth.hashers import make_password,check_password
from slack.models import Slack,User,Register
from slack.serializers import SlackSerializer,UserSerializer,RegisterSerializer,MyRegisterSerializer,MySlackRegisterSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from slack.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view

import logging
logger = logging.getLogger(__name__)

class UserSignup(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = make_password(self.request.data.get('password'))
        serializer.save(password=password)

class UserLogin(generics.GenericAPIView):

    # queryset = User.objects.all()
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):

        email = request.POST.get('email',False)
        pwd = request.POST.get('password',False)
        user = User.objects.filter(email=email)

        if user is None:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        elif not check_password(pwd,user[0].password):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        else:
            request.session['userNickname'] = user[0].nickname
            serializer = UserSerializer(user,many=True)
            print("good")
            return Response(serializer.data,status=status.HTTP_202_ACCEPTED)


# class UserDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer

class SlackList(generics.ListCreateAPIView):
    queryset = Slack.objects.all()
    serializer_class = SlackSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

    #User외래키 값 입력을 위한 오버라이딩 메소드
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SlackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Slack.objects.all()
    serializer_class = SlackSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)


class RegisterList(generics.ListCreateAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer

    #user, slack 외래키 값 입력을 위한 오버라이딩 메소드
    def perform_create(self, serializer):
        slack = Slack.objects.get(self.request.data.get('slack'))
        serializer.save(user=self.request.user,slack=slack)

class RegisterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Register.objects.all()
    serializer_class = RegisterSerializer


@api_view(['GET','POST'])
def my_register(request,pk):
    try:
        my_register = Register.objects.filter(user_id=pk)
    except Register.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = MyRegisterSerializer(my_register,many=True)
        return Response(serializer.data)


@api_view(['GET','PUT'])
def my_slack_register(request,pk):

    if request.method == "GET":
        try:
            my_slack_register = Register.objects.filter(slack_id=pk)
        except Register.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MySlackRegisterSerializer(my_slack_register,many=True)
        return Response(serializer.data)

    if request.method == "POST":

        try:
            my_slack_register = Register.objects.filter(slack_id=pk, user_id=request.data['user_id'])
        except Register.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MySlackRegisterSerializer(my_slack_register)
        if serializer.is_valid():
            serializer.save()

