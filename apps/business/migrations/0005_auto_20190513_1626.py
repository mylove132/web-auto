# Generated by Django 2.2 on 2019-05-13 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('business', '0004_pressuretest_module'),
    ]

    operations = [
        migrations.AddField(
            model_name='pressuretest',
            name='cookies',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='压测接口cookies'),
        ),
        migrations.AddField(
            model_name='pressuretest',
            name='pre_interface_request_type',
            field=models.IntegerField(blank=True, choices=[(1, 'GET'), (2, 'POST'), (3, 'DELETE')], default=1, null=True, verbose_name='压测接口请求类型'),
        ),
        migrations.AddField(
            model_name='pressuretest',
            name='pre_interface_timeout_time',
            field=models.IntegerField(blank=True, default=5000, null=True, verbose_name='压测接口类型'),
        ),
        migrations.AddField(
            model_name='pressuretest',
            name='url',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='压测接口url'),
        ),
        migrations.AlterField(
            model_name='pressuretest',
            name='pre_interface',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='压测接口'),
        ),
        migrations.AlterField(
            model_name='pressuretest',
            name='pre_interface_method',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='压测接口方法'),
        ),
        migrations.AlterField(
            model_name='pressuretest',
            name='pre_interface_param_key',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='压测接口参数key'),
        ),
        migrations.AlterField(
            model_name='pressuretest',
            name='pre_interface_param_type',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='压测接口参数类型'),
        ),
        migrations.AlterField(
            model_name='pressuretest',
            name='pre_interface_param_value',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='压测接口参数value'),
        ),
    ]