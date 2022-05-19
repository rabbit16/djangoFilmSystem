# -*- coding: utf-8 -*-
# @Time    : 2022/5/12 3:56 下午
# @Author  : rabbit
# @File    : forms.py
# @Software: PyCharm

import re

from django import forms
from django.contrib.auth import login
from django.db.models import Q
from users.models import User
from django_redis import get_redis_connection

from .constant_params import OUT_TIME

class RegisterForm(forms.Form):  # TODO 这里也要加逻辑
    username = forms.CharField(max_length=20, min_length=5, error_messages={
        "min_length": "最小长度是5位",
        "max_length": "最大长度是20位",
        "required": "用户名不能为空"
    })
    password = forms.CharField(max_length=20, min_length=5, error_messages={
        "min_length": "最小长度是5位",
        "max_length": "最大长度是20位",
        "required": "密码不能为空"
    })
    mobile = forms.CharField(max_length=11, min_length=11, error_messages={
        "min_length": "最小长度是1位",
        "max_length": "最大长度是11位",
        "required": "手机号不能为空"
    })
    email = forms.CharField(max_length=30, min_length=5, error_messages={
        "min_length": "最小长度是16位",
        "max_length": "最大长度是16位",
        "required": "email不能为空"
    })
    picCode = forms.CharField(max_length=50, min_length=4, error_messages={
        "min_length": "最小长度是4位",
        "max_length": "最大长度是50位",
        "required": "图形验证码不能为空"
    })
    picNum = forms.CharField(max_length=4, min_length=4, error_messages={
        "min_length": "最小长度是4位",
        "max_length": "最大长度是4位",
        "required": "图形验证码不能为空"
    })
    gender = forms.BooleanField(
        help_text="这个是性别，男就是True，女就是Flase",
        error_messages={
            "required": "这必须是一个bool值"
        }
    )
    real_name = forms.CharField(max_length=20, min_length=1, error_messages={
        "min_length": "最小长度是1位",
        "max_length": "最大长度是20位",
        "required": "用户名不能为空"
    })
    birthday = forms.CharField(
        max_length=50, min_length=5,
        error_messages={
            "min_length": "最小长度是1位",
            "max_length": "最大长度是20位",
            "required": "生日不正确"
        }
    )


    def clean_username_mobile(self):
        username = self.cleaned_data.get('username')
        mobile = self.cleaned_data.get('mobile')
        if User.objects.filter(Q(username=username) | Q(mobile=mobile)).exists():
            return forms.ValidationError("用户名和手机号已经被注册了，请重新输入")
        return username, mobile

    def clean_real_rname(self):
        real_name = self.cleaned_data.get("real_name")
        result = re.findall("[0-9a-zA-Z!@#$%^&*()_+><,.;':\"\'`~\，。；'【】「」\{\}?/]", real_name)
        if len(result) > 0:
            return forms.ValidationError("真实姓名不合法")
        return real_name

    # def clean_email(self):
    #     # check '@'
    #     email = self.cleaned_data.get("email")
    #     at_count = 0
    #     for element in self.cleaned_data.get("email"):
    #         if element == '@':
    #             at_count = at_count + 1
    #
    #     if at_count != 1:
    #         return forms.ValidationError("邮箱格式不正确")
    #
    #     # check ' '
    #     for element in self.cleaned_data.get("email"):
    #         if element == ' ':
    #             return forms.ValidationError("邮箱格式不正确")
    #
    #     # check '.com'
    #     # postfix = self.cleaned_data.get("email")[-4:]
    #     # if postfix != '.com':
    #     #     return forms.ValidationError("邮箱格式不正确")
    #
    #     # check char
    #     for element in email:
    #         if element.isalpha() == False and element.isdigit() == False:
    #             if element != '.' and element != '@' and element != '_':
    #                 return forms.ValidationError("邮箱格式不正确")
    #
    #     return email

    def clean(self):
        cleaned_data = super().clean()
        # password = cleaned_data.get('password')
        # password_repeat = cleaned_data.get('password_repeat')
        redis_base = get_redis_connection('verify_codes')
        picNum = cleaned_data.get('picNum')
        picNumInRedis = redis_base.get('img_{}'.format(cleaned_data.get('picCode'))).decode('utf8')
        # if password != password_repeat:
        #     return forms.ValidationError("两次密码不一致")
        if picNum != picNumInRedis:
            return forms.ValidationError("验证码输入不正确")



