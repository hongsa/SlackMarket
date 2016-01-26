from django.contrib.auth.hashers import make_password,check_password
from slack.models import Slack,User,Register
from slack.serializers import SlackSerializer,UserSerializer,RegisterSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status

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

    #User외래키 값 입력을 위한 오버라이딩 메소드
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SlackDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Slack.objects.all()
    serializer_class = SlackSerializer


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


class MyRegisterList(generics.GenericAPIView):

    queryset = Register.objects.all()
    serializer_class = RegisterSerializer

    def get(self, request, *args, **kwargs):

        registers = Register.objects.filter(user_id = request.data['id'])
        print(registers)
        return "sssss"







# class MySlackRegister(generics.GenericAPIView):