from django.contrib import admin
from .models import Slack,Register,CustomUser

# Register your models here.

class UserAdmin(admin.ModelAdmin):
    list_display = ('id','email','username')

class SlackAdmin(admin.ModelAdmin):
    list_display = ('id','name','description')

class RegisterAdmin(admin.ModelAdmin):
    list_display = ('id','type','description','user','slack')


admin.site.register(CustomUser,UserAdmin)
admin.site.register(Slack,SlackAdmin)
admin.site.register(Register,RegisterAdmin)
