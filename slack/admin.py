from django.contrib import admin
from .models import User,Slack,Register

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','nickname')

class SlackAdmin(admin.ModelAdmin):
    list_display = ('id','name','description')

class RegisterAdmin(admin.ModelAdmin):
    list_display = ('id','type','description','user','slack')


admin.site.register(User,UserAdmin)
admin.site.register(Slack,SlackAdmin)
admin.site.register(Register,RegisterAdmin)
