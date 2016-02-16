# -*- coding: utf-8 -*-
from rest_framework.response import Response
from rest_framework import status, viewsets
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

def token_required(func):
    def inner(request, *args, **kwargs):
        if request.method == 'OPTIONS':
            return func(request, *args, **kwargs)
        auth_header = request.META.get('HTTP_AUTHORIZATION', None)
        if auth_header is not None:
            tokens = auth_header.split(' ')
            if len(tokens) == 2 and tokens[0] == 'Token':
                try:
                    token = tokens[1]
                    decode = jwt_decode_handler(token)
                    print('success')
                    return func(request, *args, **kwargs)
                except:
                    print('token error')
                    return Response(status = status.HTTP_401_UNAUTHORIZED)

        print('no token')
        return Response(status = status.HTTP_401_UNAUTHORIZED)

    return inner