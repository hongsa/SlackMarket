from django.contrib import admin
from .models import User,Slack,Register

# Register your models here.

admin.site.register(User)
admin.site.register(Slack)
admin.site.register(Register)
