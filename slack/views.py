# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.hashers import make_password,check_password
from slack.models import Slack,Register,User,FacebookUser
from slack.serializers import SlackSerializer,UserSerializer,RegisterSerializer,MyRegisterSerializer,MySlackSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework_jwt.settings import api_settings
from slack.utils import token_required

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER
OAUTH_SECRET_PASSWORD = 'vpdltmqnrtktjd'
SCROLL_NUMBER = 3

import logging
logger = logging.getLogger(__name__)


@api_view(['GET','POST'])
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
        payload = jwt_payload_handler(facebook.user)
        token = jwt_encode_handler(payload)

        #serializer를 이용한 직렬화 및 토큰 추가
        serializer = UserSerializer(facebook.user)
        serializer_data = serializer.data
        serializer_data['token'] = token

        return Response(serializer_data, status=status.HTTP_202_ACCEPTED)
    except:
        user = User.objects.create_user(email,username,password)
        user.login_with_oauth=True
        user.save()
        FacebookUser(user=user, oauth_user_id=oauth_user_id, gender=gender, updated_time = updated_time,
                     locale = locale).save()
        # u = authenticate(email=email, password=password)
        # login(request,u)
        # serializer = UserSerializer(u)
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        #serializer를 이용한 직렬화 및 토큰 추가
        serializer = UserSerializer(user)
        serializer_data = serializer.data
        serializer_data['token'] = token

        return Response(serializer_data, status=status.HTTP_201_CREATED)


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
        # u = authenticate(email=email, password=password)
        # login(request,u)

        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)

        #serializer를 이용한 직렬화 및 토큰 추가
        serializer = UserSerializer(user)
        serializer_data = serializer.data
        serializer_data['token'] = token
        return Response(serializer_data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
def email_login(request):

    #값 제대로 안오면 에러
    if all(x in request.data for x in ['email', 'password']):
        email = request.data.get('email')
        password = request.data.get('password')
    else:
        return Response(status=status.HTTP_204_NO_CONTENT)

    #인증
    # u = authenticate(email=email, password=password)
    #인증되면 로그인(자동으로 세션 생성됨)
    # login(request,u)
    # 이 부분을 토큰으로 변경함

    try:
        user = User.objects.get(email=email)
        if check_password(password, user.password):

            # jwt token 생성
            payload = jwt_payload_handler(user)
            token = jwt_encode_handler(payload)

            #serializer를 이용한 직렬화 및 토큰 추가
            serializer = UserSerializer(user)
            serializer_data = serializer.data
            serializer_data['token'] = token

            return Response(serializer_data, status=status.HTTP_202_ACCEPTED)

        else:
            if User.objects.filter(email=email).count() > 0:
                #oauth 로그인 해야함
                print('social login please')
                if User.objects.filter(email=email)[0].login_with_oauth == True:
                    return Response(status=status.HTTP_409_CONFLICT)
                #패스워드 에러
                else:
                    print('password error')
                    return Response(status=status.HTTP_409_CONFLICT)
                    #해당 유저 없음
    except:
        print('no user')
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET','POST'])
@token_required
def slack_lists(request, pk):

    offset = int(pk) * SCROLL_NUMBER
    limit = (int(pk) + 1) * SCROLL_NUMBER
    slack_lists = Slack.objects.order_by('-created')[offset : limit]

    if slack_lists:
        serializer = SlackSerializer(slack_lists,many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)



@api_view(['GET','POST'])
@token_required
def slack_detail(request, pk):

    try:
        slack_detail = Slack.objects.filter(id = pk)
    except Slack.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = SlackSerializer(slack_detail,many=True)
    return Response(serializer.data, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@token_required
def register(request):

    slack_id = int(request.data.get('slack_id'))
    user_id = int(request.data.get('user_id'))

    if Register.objects.filter(slack=slack_id,user=user_id).count() > 0:
        return Response(status=status.HTTP_409_CONFLICT)

    else:
        slack = Slack.objects.get(id=slack_id)
        user = User.objects.get(id=user_id)
        description = request.data.get('description')
        Register(user=user, slack=slack, description=description).save()
        return Response(status=status.HTTP_201_CREATED)


@api_view(['POST'])
@token_required
def my_register(request, pk):

    offset = int(pk) * SCROLL_NUMBER
    limit = (int(pk) + 1) * SCROLL_NUMBER
    user_id = int(request.data)

    my_registers = Register.objects.filter(user_id = user_id).order_by('-created')[offset : limit]
    if my_registers:
        serializer = MyRegisterSerializer(my_registers,many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['POST'])
@token_required
def my_slack(request, pk):

    offset = int(pk) * SCROLL_NUMBER
    limit = (int(pk) + 1) * SCROLL_NUMBER
    user_id = int(request.data)

    my_slacks = Slack.objects.filter(user_id = user_id).order_by('-created')[offset : limit]
    if my_slacks:
        serializer = SlackSerializer(my_slacks, many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    else:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(['GET','POST'])
@token_required
def my_slack_check(request,pk):
    if request.method == "GET":
        try:
            my_slack_register = Register.objects.filter(slack_id = pk)
        except Register.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = MyRegisterSerializer(my_slack_register,many=True)
        return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

    if request.method == "POST":
        print(request.data)
        id = request.data.get('register_id')
        type = request.data.get('num')
        my_slack_register = Register.objects.get(id = id)
        my_slack_register.type = type
        my_slack_register.save()
        return Response(type, status=status.HTTP_202_ACCEPTED)


@api_view(['POST'])
@token_required
def slack_register(request):

    if all(x in request.data for x in ['name','url','token','description','type','category','user_id']):
        name = request.data.get('name')
        url = request.data.get('url')
        token = request.data.get('token')
        description = request.data.get('description')
        type = int(request.data.get('type'))
        category = request.data.get('category')
        user_id = request.data.get('user_id')

    else:
        return Response(status=status.HTTP_204_NO_CONTENT)

    Slack(name=name, url=url, token=token, description=description, type=type, category=category,
          user_id=user_id).save()
    return Response(status=status.HTTP_201_CREATED)
