from django.http import JsonResponse
from dss.Serializer import serializer
from rest_framework.views import APIView
from business.models import Module, PressureTest
from users.models import User
import json
import hashlib
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def get_page_info(params):
    pageSize = params.get('pageSize')
    pageNo = params.get('pageNo')
    if pageNo is None:
        pageNo = 1
    else:
        pageNo = int(pageNo)
    if pageSize is None:
        pageSize = 10
    else:
        pageSize = int(pageSize)

    return pageSize, pageNo


class QureyModuleByUser(APIView):
    """
    通过用户id或者用户名查询模块
    """

    def get_object(self, pk):
        try:
            if isinstance(pk, str):
                if not pk.isdigit():
                    return User.objects.get(username=pk)
                else:
                    return User.objects.get(pk=pk)
            else:
                return None
        except Exception as e:
            pass

    def get(self, request, pk):
        response = {}
        params = request.query_params
        pageSize, pageNo = get_page_info(params)
        try:
            user = self.get_object(pk)
            if not user:
                response['code'] = 2000
                response['msg'] = '查询的用户不存在'
                response['data'] = None
                return JsonResponse(response)
            module = Module.objects.filter(user_id=user.id)
            if not module:
                response['code'] = 2002
                response['msg'] = '查询的模块不存在'
                response['data'] = None
                return JsonResponse(response)
            json_date = serializer(module,
                                   include_attr=('id', 'module_name', 'module_env', 'module_type', 'create_time',
                                                 'update_time', 'module_desc'),
                                   foreign=True, datetime_format='string')
            p = Paginator(json_date, pageSize)
            try:
                contract = p.page(pageNo).object_list
            except PageNotAnInteger:
                contract = p.page(1).object_list
            except EmptyPage:
                contract = []
            response['code'] = 0
            response['msg'] = 'OK'
            response['pageNo'] = pageNo
            response['pageSize'] = pageSize
            response['moduleList'] = contract
            response['total'] = p.count
            return JsonResponse(response)
        except Exception as e:
            response['msg'] = str(e)
            response['code'] = -1
            response['data'] = None
            return JsonResponse(response)


class QureyModule(APIView):
    """
    通过模块id查找模块
    """

    def get_object(self, pk):
        try:
            if pk is not None:
                return Module.objects.filter(pk=pk).first()
            else:
                return None
        except Exception as e:
            pass

    def get(self, request, pk):
        response = {}
        try:
            module = self.get_object(pk)
            if not module:
                response['code'] = 2000
                response['msg'] = '查询的模块不存在'
                response['data'] = None
                return JsonResponse(response)
            response['code'] = 0
            response['msg'] = 'OK'
            response['data'] = serializer(module,
                                          include_attr=('id', 'module_name', 'module_env', 'module_type', 'create_time',
                                                        'update_time', 'module_desc'),
                                          foreign=True, datetime_format='string')
            return JsonResponse(response)
        except Exception as e:
            response['msg'] = str(e)
            response['code'] = -1
            response['data'] = None

    def post(self, request):
        """
        通过用户名增加或者更新模块
        :param request:
        :return:
        """
        response = {}
        try:
            if request._request.method == "POST":
                module_id = request._request.POST.get('id')
                module_name = request._request.POST.get('module_name')
                module_desc = request._request.POST.get('module_desc')
                module_type = request._request.POST.get('module_type')
                module_env = request._request.POST.get('module_env')
                user_name = request._request.POST.get('user')
                user_obj = User.objects.filter(username=user_name).first()
                user = user_obj
                import datetime
                (result, created) = Module.objects. \
                    update_or_create(pk=module_id,
                                     defaults={'user': user,
                                               'module_name': module_name,
                                               'module_type': module_type,
                                               'module_env': module_env,
                                               'module_desc': module_desc,
                                               'update_time': datetime.datetime.now()
                                               })
                if result:
                    response['code'] = 0
                    response['msg'] = 'OK'
                    response['data'] = None
                    return JsonResponse(response)
                else:
                    response['code'] = 2001
                    response['msg'] = '模版创建或者更新失败'
                    response['data'] = result
                    return JsonResponse(response)
        except Exception as e:
            response['msg'] = str(e)
            response['code'] = -1
            response['data'] = None
            return JsonResponse(response)

    def delete(self, request, pk):
        """
        通过模块id删除模块
        :param request:
        :param pk:
        :return:
        """
        response = {}
        try:
            if not self.get_object(pk):
                response['code'] = 2004
                response['msg'] = '删除的模块不存在'
                response['data'] = None
                return JsonResponse(response)

            (deleted, result) = self.get_object(pk).delete()
            if deleted:
                response['code'] = 0
                response['msg'] = 'OK'
                response['data'] = None
                return JsonResponse(response)
            else:
                response['code'] = 2003
                response['msg'] = '删除失败'
                response['data'] = result
                return JsonResponse(response)
        except Exception as e:
            response['msg'] = str(e)
            response['code'] = -1
            response['data'] = None
            return JsonResponse(response)


class QureyModuleList(APIView):
    def get(self, request):
        params = request.query_params
        pageSize, pageNo = get_page_info(params)
        response = {}
        try:
            moudle_list = Module.objects.all().filter()
            if moudle_list:
                json_date = serializer(moudle_list,
                                       include_attr=(
                                           'id', 'module_name', 'username', 'module_env', 'module_type', 'create_time',
                                           'update_time', 'module_desc', 'user_id', 'user'),
                                       foreign=True, datetime_format='string')
                p = Paginator(json_date, pageSize)
                try:
                    contract = p.page(pageNo).object_list
                except PageNotAnInteger:
                    contract = p.page(1).object_list
                except EmptyPage:
                    contract = []
                response['code'] = 0
                response['msg'] = 'OK'
                response['pageNo'] = pageNo
                response['pageSize'] = pageSize
                response['moduleList'] = contract
                response['total'] = p.count
                return JsonResponse(response)
            else:
                pass
        except Exception as e:
            response['msg'] = str(e)
            response['code'] = -1
            response['data'] = None
            return JsonResponse(response)


class QueryPressureTest(APIView):
    """
       通过模块id查找模块
       """

    def get_object(self, pk):
        try:
            if pk is not None:
                return Module.objects.filter(pk=pk).first()
            else:
                return None
        except Exception as e:
            pass

    def get(self, request, pk):
        response = {}
        params = request.query_params
        pageSize, pageNo = get_page_info(params)
        try:
            module = self.get_object(pk)
            if not module:
                response['code'] = 2000
                response['msg'] = '查询的模块不存在'
                response['data'] = None
                return JsonResponse(response)
            pressureTest = PressureTest.objects.filter(module_id=pk)
            json_date = serializer(pressureTest,
                                   include_attr=(
                                       'id', 'pre_time', 'pre_num', 'pre_type', 'pre_interface_name', 'pre_interface',
                                       'pre_interface_request_type',
                                       'pre_interface_timeout_time',
                                       'url',
                                       'response_assert',
                                       'cookies',
                                       'header',
                                       'pre_interface_method',
                                       'pre_interface_param_type', 'pre_interface_param_key',
                                       'pre_interface_param_value',
                                       'create_time', 'update_time'),
                                   foreign=True, datetime_format='string')
            p = Paginator(json_date, pageSize)
            try:
                contract = p.page(pageNo).object_list
            except PageNotAnInteger:
                contract = p.page(1).object_list
            except EmptyPage:
                contract = []
            response['code'] = 0
            response['msg'] = 'OK'
            response['pageNo'] = pageNo
            response['pageSize'] = pageSize
            response['scriptsList'] = contract
            response['total'] = p.count
            return JsonResponse(response)
        except Exception as e:
            response['msg'] = str(e)
            response['code'] = -1
            response['data'] = None
            return JsonResponse(response)


class PressureTestView(APIView):
    """
    通过模块id查找模块
    """

    def get_object(self, pk):
        try:
            if pk is not None:
                return PressureTest.objects.filter(pk=pk).first()
            else:
                return None
        except Exception as e:
            pass

    def get(self, request, pk):
        response = {}
        try:
            pressureTest = self.get_object(pk)
            if not pressureTest:
                response['code'] = 2000
                response['msg'] = '查询的脚本不存在'
                response['data'] = None
                return JsonResponse(response)
            response['code'] = 0
            response['msg'] = 'OK'
            response['data'] = serializer(pressureTest,
                                          include_attr=('id', 'pre_time', 'pre_num', 'pre_type', 'pre_interface_name',
                                                        'pre_interface',
                                                        'pre_interface_request_type',
                                                        'pre_interface_timeout_time',
                                                        'response_assert',
                                                        'url',
                                                        'header',
                                                        'cookies',
                                                        'pre_interface_method',
                                                        'pre_interface_param_type', 'pre_interface_param_key',
                                                        'pre_interface_param_value',
                                                        'create_time', 'update_time'),
                                          foreign=True, datetime_format='string')
            return JsonResponse(response)
        except Exception as e:
            response['msg'] = str(e)
            response['code'] = -1
            response['data'] = None

    def post(self, request):
        """
        通过用户名增加或者更新模块
        :param request:
        :return:
        """
        response = {}
        try:
            if request._request.method == "POST":
                pre_id = request._request.POST.get('id')
                pre_time = request._request.POST.get('pre_time')
                url = request._request.POST.get('url')
                pre_interface_request_type = request._request.POST.get('pre_interface_request_type')
                pre_interface_timeout_time = request._request.POST.get('pre_interface_timeout_time')
                cookies = request._request.POST.get('cookies')
                header = request._request.POST.get('header')
                pre_num = request._request.POST.get('pre_num')
                pre_type = request._request.POST.get('pre_type')
                pre_interface_name = request._request.POST.get('pre_interface_name')
                pre_interface = request._request.POST.get('pre_interface')
                response_assert = request._request.POST.get('response_assert')
                pre_interface_method = request._request.POST.get('pre_interface_method')
                pre_interface_param_type = request._request.POST.get('pre_interface_param_type')
                pre_interface_param_key = request._request.POST.get('pre_interface_param_key')
                pre_interface_param_value = request._request.POST.get('pre_interface_param_value')
                module_id = request._request.POST.get('module_id')
                module_obj = Module.objects.filter(id=module_id).first()
                module = module_obj
                import datetime
                (result, created) = PressureTest.objects. \
                    update_or_create(pk=pre_id,
                                     defaults={'module': module,
                                               'pre_time': pre_time,
                                               'url': url,
                                               'response_assert': response_assert,
                                               'pre_interface_request_type': pre_interface_request_type,
                                               'pre_interface_timeout_time': pre_interface_timeout_time,
                                               'cookies': cookies,
                                               'header': header,
                                               'pre_num': pre_num,
                                               'pre_type': pre_type,
                                               'pre_interface_name': pre_interface_name,
                                               'pre_interface': pre_interface,
                                               'pre_interface_method': pre_interface_method,
                                               'pre_interface_param_type': pre_interface_param_type,
                                               'pre_interface_param_key': pre_interface_param_key,
                                               'pre_interface_param_value': pre_interface_param_value,
                                               'update_time': datetime.datetime.now()
                                               })
                if result:
                    response['code'] = 0
                    response['msg'] = 'OK'
                    response['data'] = None
                    return JsonResponse(response)
                else:
                    response['code'] = 2001
                    response['msg'] = '模版创建或者更新失败'
                    response['data'] = result
                    return JsonResponse(response)
        except Exception as e:
            response['msg'] = str(e)
            response['code'] = -1
            response['data'] = None
            return JsonResponse(response)

    def delete(self, request, pk):
        """
        通过模块id删除模块
        :param request:
        :param pk:
        :return:
        """
        response = {}
        try:
            if not self.get_object(pk):
                response['code'] = 2004
                response['msg'] = '删除的脚本不存在'
                response['data'] = None
                return JsonResponse(response)

            (deleted, result) = self.get_object(pk).delete()
            if deleted:
                response['code'] = 0
                response['msg'] = 'OK'
                response['data'] = None
                return JsonResponse(response)
            else:
                response['code'] = 2003
                response['msg'] = '删除失败'
                response['data'] = result
                return JsonResponse(response)
        except Exception as e:
            response['msg'] = str(e)
            response['code'] = -1
            response['data'] = None
            return JsonResponse(response)


class ExecScripts(APIView):
    """
      通过模块id查找模块
      """

    def get_object(self, pk):
        try:
            if pk is not None:
                return PressureTest.objects.filter(pk=pk).first()
            else:
                return None
        except Exception as e:
            pass

    def get(self, request, pk):
        try:
            pre_obj: PressureTest = self.get_object(pk)
            request_type = pre_obj.pre_type
            if request_type == 1:
                """
                处理http接口
                """
                pre_num = pre_obj.pre_num
                pre_time = pre_obj.pre_time
                url = pre_obj.url
                request_type = pre_obj.pre_interface_request_type
                pre_name = pre_obj.pre_interface_name
                pre_interface_params = pre_obj.pre_interface_param_value
                pre_timeOut = pre_obj.pre_interface_timeout_time
                module_id = pre_obj.module_id
                cookie = pre_obj.cookies
                header = pre_obj.header
                response_assert = pre_obj.response_assert
                if pre_interface_params:
                    pre_interface_params = json.loads(pre_interface_params)
                else:
                    pre_interface_params = {}

                if cookie:
                    cookie = json.loads(cookie)
                else:
                    cookie = {}

                if header:
                    header = json.loads(header)
                else:
                    header = {}

                type_dict = {1:"GET",2:"POST",3:"DELETE"}
                from business.util import jmx_http_template as jmx_http
                tem_jmx = ''
                tem_jmx = jmx_http.jmx_header_setting() + jmx_http.jmx_control_seeting(pre_num=pre_num,
                                                                                       pre_time=pre_time) + jmx_http.jmx_http_setting(
                        url, interface_name=pre_name,
                        request_type=type_dict[request_type],
                        timeOut=pre_timeOut,
                        params=pre_interface_params) + jmx_http.jmx_response_assert(
                        response_assert) + jmx_http.jmx_see_result_control() + jmx_http.result_polymerization_control() + jmx_http.requestid_bean_shell_control() + jmx_http.cookie_control(
                        list(cookie), url=url) + jmx_http.header_control(list(header))+jmx_http.jmx_end()
                print(tem_jmx)
                import business.util.constant as constant
                with open(constant.jmx_file_path+'file.jmx','w') as jmx_file:
                    jmx_file.write(tem_jmx)
            elif request_type == 2:
                """
                处理dubbo接口
                """
                pass
            elif request_type == 3:
                """
                处理socket接口
                """
                pass
            else:
                pass
        except Exception as e:
            import traceback
            print('--------------------')
            print(traceback.print_exc())
            print(e)
