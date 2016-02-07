from django.forms import widgets
from rest_framework import serializers
from slack.models import Slack,Register,User

# model에 저장된 값을 직렬화 하는 부분
# object를 가져와서 데이터 형식에 맞게 변환

class UserSerializer(serializers.ModelSerializer):

    # model에 related_name으로 변수 설정해야함
    # user와 연결된 slack을 보여준다 slack부분에 외래키 설정되어있지만 반대형태로 이렇게 보여줌
    slack_user =serializers.PrimaryKeyRelatedField(many=True,queryset=Slack.objects.all())
    register_user =serializers.PrimaryKeyRelatedField(many=True,queryset=Register.objects.all())

    #meta 클래스에서 key값을 보여준다
    #fields 지정하는 것이 model 필드 값과 연결됨. api에서 보여지는 것 추가됨
    class Meta:
        model = User
        fields = ('id','email','username','password','slack_user','register_user')

class SlackSerializer(serializers.ModelSerializer):

    # 외래키로 연결된 user부분을 보여준다. 그러나 값을 입력은 불가, 왜냐면 자동으로 로그인되어있는 user값으로 들어가기 때문
    user_id = serializers.ReadOnlyField(source='user.id')
    user_nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = Slack
        fields = ('id','name','url','token','description','type','category','created','user_id','user_nickname')

class RegisterSerializer(serializers.ModelSerializer):

    #외래키로 연결된 user,slack 부분. 로그인과 선택되어있는 slack값이 default값으로 들어가므로 수정 불가능.
    user = serializers.ReadOnlyField(source='user.id')
    slack = serializers.ReadOnlyField(source='slack.id')
    class Meta:
        model = Register
        fields = ('id','type','description','created','user','slack')

class MyRegisterSerializer(serializers.ModelSerializer):

    slack_name = serializers.ReadOnlyField(source='slack.name')
    user_nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = Register
        fields = ('id','type','description','created','slack_name','user_nickname')

class MySlackRegisterSerializer(serializers.ModelSerializer):
    slack_name = serializers.ReadOnlyField(source='slack.name')
    user_nickname = serializers.ReadOnlyField(source='user.nickname')

    class Meta:
        model = Register
        fields = ('id','type','description','slack_name','user_nickname')