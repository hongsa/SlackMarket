from django.forms import widgets
from rest_framework import serializers
from slack.models import Slack,User,Register

# model에 저장된 값을 직렬화 하는 부분
# object를 가져와서 데이터 형식에 맞게 변환

class UserSerializer(serializers.ModelSerializer):

    # model에 related_name으로 변수 설정해야함
    # user와 연결된 slack을 보여준다 slack부분에 외래키 설정되어있지만 반대형태로 이렇게 보여줌
    slack_user =serializers.PrimaryKeyRelatedField(many=True,queryset=Slack.objects.all())
    register_user =serializers.PrimaryKeyRelatedField(many=True,queryset=Register.objects.all())

    #meta 클래스에서 key값을 보여준다
    class Meta:
        model = User
        fields = ('id','email','nickname','password','name','age','sex','created','slack_user','register_user')

class SlackSerializer(serializers.ModelSerializer):

    # 외래키로 연결된 user부분을 보여준다. 그러나 값을 입력은 불가
    user = serializers.ReadOnlyField(source='user.id')

    class Meta:
        model = Slack
        fields = ('id','name','url','token','description','type','category','created','user')

class RegisterSerializer(serializers.ModelSerializer):

    user = serializers.ReadOnlyField(source='user.id')
    slack = serializers.ReadOnlyField(source='slack.id')
    class Meta:
        model = Register
        fields = ('id','type','description','created','user','slack')