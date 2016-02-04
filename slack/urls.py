from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from slack import views

urlpatterns = [
    url(r'^slacks/$', views.SlackList.as_view()),
    url(r'^slacks/(?P<pk>[0-9]+)/$', views.SlackDetail.as_view()),
    # url(r'^signup/$', views.UserSignup.as_view()),
    url(r'^signup/$', views.signup),

    url(r'^login/$', views.UserLogin.as_view()),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^registers/$', views.RegisterList.as_view()),
    url(r'^registers/(?P<pk>[0-9]+)/$', views.RegisterDetail.as_view()),
    url(r'^myregisters/(?P<pk>[0-9]+)/$', views.my_register),
    # url(r'^myregisters/(?P<pk>[0-9]+)/$', views.MyRegisterList.as_view()),
    url(r'^myslacks/(?P<pk>[0-9]+)/$', views.my_slack_register),

    #facebook login test

]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]