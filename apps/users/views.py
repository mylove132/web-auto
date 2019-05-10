from django.http import JsonResponse
from rest_framework.views import APIView

from .models import User, Token
import hashlib


def md5(name, salt='okay'):
    md5 = hashlib.md5(bytes(name, encoding='utf-8'))
    md5.update(bytes(salt, encoding='utf-8'))
    return md5.hexdigest()


class LoginView(APIView):
    authentication_classes = []

    def post(self, request):
        response = {}
        try:
            user = request._request.POST.get('user')
            password = request._request.POST.get('password')
            print(user)
            print(password)
            print(user is None or password is None)
            if (user is None or password is None):
                response['code'] = 1001
                response['msg'] = '请检查用户名密码字段'
                response['data'] = None
                return JsonResponse(response)
            import re
            p = re.compile(r"[^@]+@[^@]+\.[^@]+")
            if p.match(user):
                user_obj = User.objects.filter(email=user, password=password).first()
            else:
                user_obj = User.objects.filter(username=user, password=password).first()
            import datetime
            token_update_time= datetime.datetime.now()
            if user_obj:
                token = md5(user,salt=token_update_time.strftime('%Y-%m-%d %H:%M:%S'))
                response['code'] = 0
                response['msg'] = 'OK'
                response['data'] = {
                    "token": token,
                    'user':user_obj.username
                }
                Token.objects.update_or_create(user=user_obj,
                                               defaults={'token': token, 'update_time': token_update_time})
                return JsonResponse(response,json_dumps_params={'ensure_ascii':False})
            else:
                response['code'] = 1002
                response['msg'] = '请检查用户名密码'
                response['data'] = None
                return JsonResponse(response)
        except Exception as e:
            response['msg'] = str(e)
            response['code'] = -1
            response['data'] = None
            return JsonResponse(response)
