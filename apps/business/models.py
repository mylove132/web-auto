from django.db import models
from users.models import User
from django.utils import timezone

class Module(models.Model):
    '''
    模块数据
    '''
    module_type_index = (
        (1, '教师空间'),
        (2, '教师pad'),
        (3, '学生pad'),
        (4, '商城'),
    )
    '''
       项目环境
       '''
    module_env_index = (
        (1, 'dev'),
        (2, 'docker-dev'),
        (3, 'docker-hotfix'),
        (4, 'stress'),
    )

    module_name = models.CharField(max_length=30, verbose_name='模块名称', null=False, blank=False)
    module_type = models.IntegerField(choices=module_type_index, verbose_name='模块类型', default=1)
    module_env = models.IntegerField(choices=module_env_index, verbose_name='项目环境', default=1)
    create_time = models.DateTimeField(auto_now_add=True,verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now_add=True,verbose_name='更新时间')
    module_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name='模块描述', default='')
    user = models.ForeignKey(User,related_name='user',on_delete=models.CASCADE,default=1)

    class Meta:
        db_table = 'entity_module'
        verbose_name = '模块'


class PressureTest(models.Model):
    '''
    压力测试参数
    '''
    pre_type_index = (
        (1,'http'),
        (2,'dubbo'),
        (3,'websocket')
    )

    pre_time = models.IntegerField(default=200,verbose_name='压测时长')
    pre_num = models.IntegerField(default=100, verbose_name='并发数')
    pre_type = models.IntegerField(choices=pre_type_index,default=1,verbose_name='压测接口类型')
    pre_interface_name = models.CharField(max_length=20,blank=False, null=False, verbose_name='压测接口名称')
    pre_interface = models.CharField(max_length=100, blank=False,null=False,verbose_name='压测接口')
    pre_interface_method = models.CharField(max_length=50,blank=False,null=False,verbose_name='压测接口方法')
    pre_interface_param_type = models.CharField(max_length=100,verbose_name='压测接口参数类型')
    pre_interface_param_key = models.CharField(max_length=100,verbose_name='压测接口参数key')
    pre_interface_param_value = models.CharField(max_length=100, verbose_name='压测接口参数value')
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now_add=True, verbose_name='更新时间')
    module = models.ForeignKey(Module, related_name='module', on_delete=models.CASCADE, default=1)

    class Meta:
        db_table = 'entity_pressure_test'
        verbose_name = '模块'