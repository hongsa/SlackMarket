from django.db import models
from pygments.lexers import get_all_lexers,get_lexer_by_name
from pygments.formatters.html import HtmlFormatter
from pygments.styles import get_all_styles
from pygments import highlight

#사용자 테이블
class User(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(unique=True)
    nickname = models.CharField(max_length=100,unique=True)
    password = models.CharField(max_length=150,)
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    #0-남자, 1-여자
    sex = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)

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
    user =models.ForeignKey('User',on_delete=models.CASCADE,related_name='slack_user')

    def save(self, *args, **kwargs):
        super(Slack, self).save(*args, **kwargs)

#슬랙 등록 테이블
class Register(models.Model):
    id = models.AutoField(primary_key=True)
    # 0-대기, 1-승인, 2-거절
    type = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    #foreignkey
    user =models.ForeignKey('User',on_delete=models.CASCADE,related_name='register_user')
    slack = models.ForeignKey('Slack',on_delete=models.CASCADE,related_name='register_slack')

    def save(self, *args, **kwargs):
        super(Register, self).save(*args, **kwargs)


# LEXERS = [item for item in get_all_lexers() if item[1]]
# LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
# STYLE_CHOICES = sorted((item, item) for item in get_all_styles())
#
#
# class Slack(models.Model):
#     created = models.DateTimeField(auto_now_add=True)
#     title = models.CharField(max_length=100, blank=True, default='')
#     code = models.TextField()
#     linenos = models.BooleanField(default=False)
#     language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
#     style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
#     owner = models.ForeignKey('auth.User', related_name='slack')
#     highlighted = models.TextField()
#
#     class Meta:
#         ordering = ('created',)
#
#     def save(self, *args, **kwargs):
#         """
#         `pygments` 라이브러리를 사용하여 하이라이트된 코드를 만든다.
#         """
#         lexer = get_lexer_by_name(self.language)
#         linenos = self.linenos and 'table' or False
#         options = self.title and {'title': self.title} or {}
#         formatter = HtmlFormatter(style=self.style, linenos=linenos,
#                                   full=True, **options)
#         self.highlighted = highlight(self.code, lexer, formatter)
#         super(Slack, self).save(*args, **kwargs)