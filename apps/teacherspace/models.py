from django.db import models


class User(models.Model):
    user_type_index = (
        (1,'普通用户'),
        (2,'vip用户'),
        (3,'管理员用户')
    )
    username = models.CharField(max_length=30,verbose_name='用户名',blank=False,null=False,unique=True)
    password = models.CharField(max_length=100,verbose_name='用户密码',blank=False,null=False)
    user_type = models.IntegerField(choices=user_type_index,default=1)
    create_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'user'
        verbose_name='用户'

class Module(models.Model):
    module_type_index = (
        (1, '教师空间'),
        (2, '教师pad'),
        (3, '学生pad'),
        (4, '商城'),
    )

    module_name = models.CharField(max_length=30, verbose_name='模块名称', null=False, blank=False)
    module_type = models.IntegerField(choices=module_type_index, verbose_name='模块类型', default=1)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now_add=True)
    module_desc = models.CharField(max_length=200, blank=True, null=True, verbose_name='模块描述', default='')
    user = models.ForeignKey(User,related_name='user',on_delete=models.CASCADE,default=1)

    class Meta:
        db_table = 'module'
        verbose_name = '模块'
