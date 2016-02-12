# -*- coding: utf-8 -*-
# from slack.models import Slack
# from slack.serializers import SlackSerializer,UserSerializer
# from django.contrib.auth.models import User
# from rest_framework import mixins,generics
# from rest_framework import viewsets,renderers
# from rest_framework.response import Response
# from rest_framework.decorators import detail_route
# from rest_framework import permissions
# from slack.permissions import IsOwnerOrReadOnly
#
# class SlackViewSet(viewsets.ModelViewSet):
#     """
#     이 뷰셋은 `list`와 `create`, `retrieve`, `update`, 'destroy` 기능을 자동으로 지원합니다
#
#     여기에 `highlight` 기능의 코드만 추가로 작성했습니다
#     """
#     queryset = Slack.objects.all()
#     serializer_class = SlackSerializer
#     permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                           IsOwnerOrReadOnly,)
#
#     @detail_route(renderer_classes=[renderers.StaticHTMLRenderer])
#     def highlight(self, request, *args, **kwargs):
#         slack = self.get_object()
#         return Response(slack.highlighted)
#
#     def perform_create(self, serializer):
#             serializer.save(owner=self.request.user)
#
# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     """
#     이 뷰셋은 `list`와 `detail` 기능을 자동으로 지원합니다
#     """
#     queryset = User.objects.all()
#     serializer_class = UserSerializer
#
#
#
#
#
#
# # class SlackList(generics.ListCreateAPIView):
# #     queryset = Slack.objects.all()
# #     serializer_class = SlackSerializer
# #     # permission_classes = (permissions.IsAuthenticatedOrReadOnly)
# #
# #     # def perform_create(self, serializer):
# #     #     serializer.save(owner=self.request.user)
# #
# #
# # class SlackDetail(generics.RetrieveUpdateDestroyAPIView):
# #     queryset = Slack.objects.all()
# #     serializer_class = SlackSerializer
# #     # permission_classes = (permissions.IsAuthenticatedOrReadOnly)
#
# # class UserList(generics.ListAPIView):
# #     queryset = User.objects.all()
# #     serializer_class = UserSerializer
# #
# #
# # class UserDetail(generics.RetrieveAPIView):
# #     queryset = User.objects.all()
# #     serializer_class = UserSerializer
#
#
#
#
# # class SlackList(mixins.ListModelMixin,
# #                   mixins.CreateModelMixin,
# #                   generics.GenericAPIView):
# #     queryset = Slack.objects.all()
# #     serializer_class = SlackSerializer
# #
# #     def get(self, request, *args, **kwargs):
# #         return self.list(request, *args, **kwargs)
# #
# #     def post(self, request, *args, **kwargs):
# #         return self.create(request, *args, **kwargs)
# #
# # class SlackDetail(mixins.RetrieveModelMixin,
# #                     mixins.UpdateModelMixin,
# #                     mixins.DestroyModelMixin,
# #                     generics.GenericAPIView):
# #     queryset = Slack.objects.all()
# #     serializer_class = SlackSerializer
# #
# #     def get(self, request, *args, **kwargs):
# #         return self.retrieve(request, *args, **kwargs)
# #
# #     def put(self, request, *args, **kwargs):
# #         return self.update(request, *args, **kwargs)
# #
# #     def delete(self, request, *args, **kwargs):
# #         return self.destroy(request, *args, **kwargs)
#
#
# # class SlackList(APIView):
# #     """
# #     코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
# #     """
# #     def get(self, request, format=None):
# #         slack= Slack.objects.all()
# #         serializer = SlackSerializer(slack, many=True)
# #         return Response(serializer.data)
# #
# #     def post(self, request, format=None):
# #         serializer = SlackSerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# # class SlackDetail(APIView):
# #     """
# #     코드 조각 조회, 업데이트, 삭제
# #     """
# #     def get_object(self, pk):
# #         try:
# #             return Slack.objects.get(pk=pk)
# #         except Slack.DoesNotExist:
# #             raise Http404
# #
# #     def get(self, request, pk, format=None):
# #         slack = self.get_object(pk)
# #         serializer = SlackSerializer(slack)
# #         return Response(serializer.data)
# #
# #     def put(self, request, pk, format=None):
# #         slack = self.get_object(pk)
# #         serializer = SlackSerializer(slack, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #
# #     def delete(self, request, pk, format=None):
# #         slack = self.get_object(pk)
# #         slack.delete()
# #         return Response(status=status.HTTP_204_NO_CONTENT)