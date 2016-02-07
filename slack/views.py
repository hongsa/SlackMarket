from django.shortcuts import render
from django.contrib.auth.hashers import make_password,check_password
from slack.models import Slack,Register,User,FacebookUser
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

OAUTH_SECRET_PASSWORD = 'vpdltmqnrtktjd'

@api_view(['POST'])
def facebook(request):

    #값이 제대로 안오면 에러
    if all(x in request.data for x in ['email','name','gender','updated_time','locale']):
        email = request.data.get('email')
        username = request.data.get('name')
        gender = request.data.get('gender')
        updated_time = request.data.get('updated_time')
        locale = request.data.get('locale')
        oauth_user_id = request.data.get('id')
        password = OAUTH_SECRET_PASSWORD
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)

    #아이디가 있으면 로그인 없으면 생성
    try:
        facebook = FacebookUser.objects.get(oauth_user_id=str(oauth_user_id))
        u = authenticate(email=facebook.user.email,password=OAUTH_SECRET_PASSWORD)
        login(request,u)
        return Response(status=status.HTTP_202_ACCEPTED)
    except:
        user = User.objects.create_user(email,username,password)
        user.login_with_oauth=True
        user.save()
        FacebookUser(user=user, oauth_user_id=oauth_user_id, gender=gender, updated_time = updated_time,
                         locale = locale).save()
        u = authenticate(email=email, password=password)
        login(request,u)
        return Response(status=status.HTTP_201_CREATED)

@api_view(['POST'])
def email_signup(request):

    #값이 제대로 안오면 에러
    if all(x in request.data for x in ['email','username','password']):
        email = request.data.get('email')
        username = request.data.get('username')
        password = request.data.get('password')
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)

    #이메일 중복 체크
    if User.objects.filter(email=email).count() > 0:
        return Response(status=status.HTTP_409_CONFLICT)
    #닉네임 중복 체크
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

    #값 제대로 안오면 에러
    if all(x in request.data for x in ['email', 'password']):
        email = request.data.get('email')
        password = request.data.get('password')
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)

    u = authenticate(email=email, password=password)

    #인증되면 로그인
    if u:
        login(request,u)
        return Response(status=status.HTTP_202_ACCEPTED)

    else:
        if User.objects.filter(email=email).count() > 0:
            #oauth 로그인 해야함
            if User.objects.filter(email=email)[0].login_with_oauth == True:
                return Response(status=status.HTTP_409_CONFLICT)
            #패스워드 에러
            else:
                return Response(status=status.HTTP_409_CONFLICT)
        #해당 유저 없음
        else:
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

