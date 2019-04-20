from dss.Serializer import serializer
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from teacherspace.models import Module,User
import logging


@require_http_methods(['GET'])
def get_module_by_id(request, id):
    logger = logging.getLogger('web.auto.views')
    logger.info('请求的url:{}'.format(request.path))
    response = {}
    try:
        module = Module.objects.filter(id=id).first()
        response['code'] = 0
        response['msg'] = 'OK'
        response['data'] = serializer(module,include_attr=('module_name','get_module_type_display','create_time',
                                                           'update_time','user','username','module_desc'),foreign=True, datetime_format='string')
        logger.info('请求返回的数据:{}'.format(str(response)))
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = -1
        response['data'] = None
        logger.info('请求返回错误:{}'.format(str(response)))

    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


@require_http_methods(['GET'])
def get_module_by_username(request, username):
    logger = logging.getLogger('web.auto.views')
    print(username)
    logger.info('请求的url:{}'.format(request.path))
    response = {}
    try:
        user_id = User.objects.filter(username=username).first().id
        module = Module.objects.filter(user_id=user_id)
        response['code'] = 0
        response['msg'] = 'OK'
        response['data'] = serializer(module,include_attr=('module_name','get_module_type_display','create_time',
                                                           'update_time','user','username','module_desc'),foreign=True, datetime_format='string')
        logger.info('请求返回的数据:{}'.format(str(response)))
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = -1
        response['data'] = None
        logger.info('请求返回错误:{}'.format(str(response)))

    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})


@require_http_methods(['GET'])
def get_module_list(request):
    response = {}
    try:
        module = Module.objects.all()
        response['code'] = 0
        response['msg'] = 'OK'
        response['data'] = serializer(module,include_attr=('module_name','get_module_type_display','create_time',
                                                           'update_time','user','username','module_desc'),foreign=True, datetime_format='string')
    except Exception as e:
        response['msg'] = str(e)
        response['code'] = -1
        response['data'] = None

    return JsonResponse(response, json_dumps_params={'ensure_ascii': False})
