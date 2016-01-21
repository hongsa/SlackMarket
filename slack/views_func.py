# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from slack.models import Slack
# from slack.serializers import SlackSerializer
#
# # class JSONResponse(HttpResponse):
# #     """
# #     콘텐츠를 JSON으로 변환한 후 HttpResponse 형태로 반환합니다.
# #     """
# #     def __init__(self, data, **kwargs):
# #         content = JSONRenderer().render(data)
# #         kwargs['content_type'] = 'application/json'
# #         super(JSONResponse, self).__init__(content, **kwargs)
#
# @api_view(['GET','POST'])
# def slack_list(request,format=None):
#     """
#     코드 조각을 모두 보여주거나 새 코드 조각을 만듭니다.
#     """
#     if request.method == 'GET':
#         slack = Slack.objects.all()
#         serializer = SlackSerializer(slack, many=True)
#         return Response(serializer.data)
#
#     elif request.method == 'POST':
#         serializer = SlackSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
# @api_view(['GET','PUT','DELETE'])
# def slack_detail(request, pk,format=None):
#     """
#     코드 조각 조회, 업데이트, 삭제
#     """
#     try:
#         slack = Slack.objects.get(pk=pk)
#     except Slack.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = SlackSerializer(slack)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         # data = JSONParser().parse(request)
#         serializer = SlackSerializer(slack, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     elif request.method == 'DELETE':
#         slack.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
