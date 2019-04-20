# Generated by Django 2.2 on 2019-04-19 21:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('teacherspace', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=30, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=100, verbose_name='用户密码')),
                ('user_type', models.IntegerField(choices=[(1, '普通用户'), (2, 'vip用户'), (3, '管理员用户')], default=1)),
            ],
            options={
                'verbose_name': '用户',
                'db_table': 'user',
            },
        ),
        migrations.AddField(
            model_name='module',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user', to='teacherspace.User'),
        ),
    ]
