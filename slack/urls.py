from django.conf.urls import url,include
from rest_framework.urlpatterns import format_suffix_patterns
from slack import views

urlpatterns = [
    url(r'^slacks/$', views.SlackList.as_view()),
    url(r'^slacks/(?P<pk>[0-9]+)/$', views.SlackDetail.as_view()),
    url(r'^signup/$', views.UserSignup.as_view()),
    url(r'^login/$', views.UserLogin.as_view()),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^registers/$', views.RegisterList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls',
                               namespace='rest_framework')),
]


# from django.conf.urls import url,include
# from rest_framework.urlpatterns import format_suffix_patterns
# from slack import views_class
# from rest_framework.routers import DefaultRouter



# urlpatterns = [
#     url(r'^slacks/$', views.slack_list),
#     url(r'^slacks/(?P<pk>[0-9]+)/$', views.slack_detail),
# ]
# urlpatterns = [
#     url(r'^slacks/$', views_class.SlackList.as_view()),
#     url(r'^slacks/(?P<pk>[0-9]+)/$', views_class.SlackDetail.as_view()),
#     url(r'^users/$', views_class.UserList.as_view()),
#     url(r'^users/(?P<pk>[0-9]+)/$', views_class.UserDetail.as_view()),
#
# ]

# urlpatterns += [
#     url(r'^api-auth/', include('rest_framework.urls',
#                                namespace='rest_framework')),
# ]
#
# urlpatterns = format_suffix_patterns(urlpatterns)



# 라우터를 생성하고 뷰셋을 등록합니다
# router = DefaultRouter()
# router.register(r'slacks', views_class.SlackViewSet)
# router.register(r'users', views_class.UserViewSet)

# 이제 API URL을 라우터가 자동으로 인식합니다
# 추가로 탐색 가능한 API를 구현하기 위해 로그인에 사용할 URL은 직접 설정을 했습니다
# urlpatterns = [
#     url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework'))
# ]