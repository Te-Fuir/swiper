from django.shortcuts import render
from django.http import JsonResponse
from django.core.cache import cache

from lib.sms import send_sms
from common import errors
from lib.http import render_json
from common import keys
from user.models import User


def submit_phone(request):
    """提交手机号码, 发送验证码"""
    phone = request.POST.get('phone')
    # 发送验证码
    status, msg = send_sms(phone)
    if not status:
        return render_json(code=errors.SMS_ERROR, data='短信发送失败')
    # 发送成功
    return render_json()


def submit_vcode(request):
    """提交短信验证码"""
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')
    # 从缓存中取出vcode
    cached_vcode = cache.get(keys.VCODE_KEY % phone)

    if vcode == cached_vcode:
        # 说明验证码正确, 可以登录或者注册
        # try:
        #     user = User.objects.get(phonenum=phone)
        # except User.DoesNotExist:
        #     # 说明是注册
        #     user = User.objects.create(phonenum=phone, nickname=phone)

        user, _ = User.objects.get_or_create(phonenum=phone, defaults={'nickname': phone})
        # 把用户的id存入session中, 完成登录
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        # 验证码错误
        return render_json(code=errors.VCODE_ERROR, data='验证码错误')


def get_profile(request):
    uid = request.session.get('uid')
    if not uid:
        return render_json(code=errors.LOGIN_REQUIRED, data='请登录')
    user = User.objects.get(id=uid)
    return render_json(data=user.profile.to_dict())