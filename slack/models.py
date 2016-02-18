# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.conf import settings

#custom-user model manager
class MyUserManager(BaseUserManager):

    def create_user(self, email, username, password):
        """
        Creates and saves a User with the given email and password
        """
        if not email:
            raise ValueError('User must have an email address')

        if not username:
            raise ValueError('User must have an username')

        if not password:
            raise ValueError('User must have a password')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        """
        Creates and saves a superuser
        """
        user = self.create_user(
            email=self.normalize_email(email),
            username=username,
            password=password
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


#custom 사용자 테이블
class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    username = models.CharField(
        verbose_name='Username',
        max_length=30,
        unique=True,
        null=False
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    login_with_oauth = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    # REQUIRED_FIELDS = ['username','password']

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin


class FacebookUser(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='facebook_user')
    platform_choices = (
        ('facebook', 'Facebook'),
    )
    platform = models.CharField(
        max_length = 10,
        choices = platform_choices,
        default = 'facebook'
    )
    oauth_user_id = models.CharField(
        max_length = 30
    )
    updated_time = models.DateTimeField(
        auto_now = True
    )
    gender = models.CharField(max_length=10,default='male')
    locale = models.CharField(max_length=50,default=0)


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
    is_check = models.BooleanField(default=False)

    #foreignkey
    user =models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='register_user')
    slack = models.ForeignKey('Slack',on_delete=models.CASCADE,related_name='register_slack')

    def __str__(self):
        return self.description

    def save(self, *args, **kwargs):
        super(Register, self).save(*args, **kwargs)