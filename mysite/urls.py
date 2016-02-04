from django.conf.urls import url, include
from django.contrib import admin

from rest_framework import routers
from slack import views_func

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# 우리가 만든 API를 자동으로 라우팅합니다.
# 그리고 API 탐색을 위해 로그인 URL을 추가했습니다.
urlpatterns = [
    # url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('slack.urls')),
    url(r'^accounts/', include('allauth.urls')),
]

