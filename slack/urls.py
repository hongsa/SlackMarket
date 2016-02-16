# -*- coding: utf-8 -*-
from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from slack import views
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    url(r'^facebook/$', views.facebook),
    url(r'^signup/$', views.email_signup),
    url(r'^login/$', views.email_login),
    url(r'^lists/(?P<pk>[0-9]+)/$', views.slack_lists),
    url(r'^slacks/(?P<pk>[0-9]+)/$', views.slack_detail),
    url(r'^register/$', views.register),
    url(r'^myregisters/$', views.my_register),
    url(r'^myslacks/$', views.my_slack),
    url(r'^myslacks/(?P<pk>[0-9]+)/$', views.my_slack_register),

    #facebook login test

]

urlpatterns = format_suffix_patterns(urlpatterns)
# urlpatterns += [
#     url(r'^api-auth/', include('rest_framework.urls',
#                                namespace='rest_framework')),
# ]