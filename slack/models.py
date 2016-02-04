from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings


#사용자 테이블
# class User(models.Model):
#     id = models.AutoField(primary_key=True)
#     email = models.EmailField(unique=True)
#     nickname = models.CharField(max_length=100,unique=True)
#     password = models.CharField(max_length=150)
#     name = models.CharField(max_length=50)
#     age = models.IntegerField(blank=True)
#     # 남자-male, 여자 = female
#     gender = models.IntegerField()
#     created = models.DateTimeField(auto_now_add=True)
#
#     def __str__(self):
#         return self.email

class CustomUser(AbstractUser):
    """
    User profile which extends AbstractBaseUser class
    AbstractBaseUser contains basic fields like password and last_login
    """
    age = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(default='female',
                              max_length=20, blank=True)
    # to enforce that you require email field to be associated with
    # every user at registration
    REQUIRED_FIELDS = ["email"]


#슬랙 테이블
class Slack(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    url = models.CharField(unique=True,max_length=200)
    token = models.CharField(max_length=100,unique=True)
    description = models.TextField()
    # 0-공개초대, 1-승인초대, 2-초대거부
    type = models.IntegerField()
    category = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    #foreignkey
    user =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='slack_user')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Slack, self).save(*args, **kwargs)

#슬랙 등록 테이블
class Register(models.Model):
    id = models.AutoField(primary_key=True)
    # 0-대기, 1-승인, 2-거절
    type = models.IntegerField(default=0)
    description = models.TextField(default="")
    created = models.DateTimeField(auto_now_add=True)
    #foreignkey
    user =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='register_user')
    slack = models.ForeignKey('Slack',on_delete=models.CASCADE,related_name='register_slack')

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        super(Register, self).save(*args, **kwargs)