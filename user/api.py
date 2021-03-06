import logging

from django.core.cache import cache

from lib.sms import send_sms
from common import errors
from lib.http import render_json
from common import keys
from user.forms import ProfileModelForm
from user.logic import handle_upload
from user.models import User

logger_info = logging.getLogger('inf')
logger_error = logging.getLogger('err')


def submit_phone(request):
    """提交手机号码, 发送验证码"""
    phone = request.POST.get('phone')
    # 发送验证码
    send_sms.delay(phone)

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
        #     user = User.get(phonenum=phone)
        # except User.DoesNotExist:
        #     # 说明是注册
        #     user = User.objects.create(phonenum=phone, nickname=phone)

        user, _ = User.get_or_create(phonenum=phone, defaults={'nickname': phone})
        # 把用户的id存入session中, 完成登录
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    else:
        # 验证码错误
        raise errors.VcodeError


def get_profile(request):
    """获取个人资料"""
    return render_json(data=request.user.profile.to_dict())


def edit_profile(request):
    """修改个人资料"""
    form = ProfileModelForm(request.POST)
    if form.is_valid():
        # 可以接受并保存
        profile = form.save(commit=False)
        uid = request.user.id
        profile.id = uid
        profile.save()
        # 更新缓存
        cache.set(keys.PROFILE_KEY % uid, profile, 86400 * 14)

        logger_info.info(f'{request.user.nickname} modify profile success')

        return render_json(data=profile.to_dict())
    else:
        logger_error.error(f'{request.user.nickname} modify profile error')
        raise errors.ProfileError


def upload_avatar(request):
    """上传个人头像"""
    # 获取上传图片数据
    avatar = request.FILES.get('avatar')
    # 保存到指定的位置, 分块写入本地
    user = request.user
    handle_upload.delay(user, avatar)
    return render_json()
