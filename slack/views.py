from django.shortcuts import render
from django.contrib.auth.hashers import make_password,check_password
from slack.models import Slack,Register,User
from slack.serializers import SlackSerializer,UserSerializer,RegisterSerializer,MyRegisterSerializer,MySlackRegisterSerializer
from rest_framework import generics
from rest_framework import permissions
from rest_framework.response import Response
from rest_framework import status
from slack.permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required

import logging
logger = logging.getLogger(__name__)


@api_view(['POST'])
def email_signup(request):

    if all(x in request.data for x in ['email','username','password']):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)

    if User.objects.filter(email=email).count() > 0:
        return Response(status=status.HTTP_409_CONFLICT)
    elif User.objects.filter(username=username).count() > 0:
        return Response(status=status.HTTP_409_CONFLICT)
    else:
        user = User.objects.create_user(email,username,password)
        user.save()
        u = authenticate(email=email, password=password)
        login(request,u)
        return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
def email_login(request):

    if all(x in request.data for x in ['email', 'password']):
        email = request.data.get('email')
        password = request.data.get('password')
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)

    u = authenticate(email=email, password=password)

    if u:
        print("login")
        login(request,u)
        return Response(status=status.HTTP_202_ACCEPTED)

    else:
        if User.objects.filter(email=email).count() > 0:

            if User.objects.filter(email=email)[0].login_with_oauth == True:
                print("oauth go")
                return Response(status=status.HTTP_409_CONFLICT)
            else:
                print("password error")
                return Response(status=status.HTTP_409_CONFLICT)
        else:
            print("no user")
            return Response(status=status.HTTP_204_NO_CONTENT)


class SlackList(generics.ListCreateAPIView):
    queryset = Slack.objects.all()
    serializer_class = SlackSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly)

    #User외래키 값 입력을 위한 오버라이딩 메소드
    def perform_create(self, serializer):
        print(self.request.user)
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
        print(self.request.data.get('slack'))
        print(self.request.user)
        id = self.request.data.get('slack')
        id = 2
        slack = Slack.objects.get(id=id)

        serializer.save(user=self.request.user, slack=slack)

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

