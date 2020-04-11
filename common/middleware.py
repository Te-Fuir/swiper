from django.utils.deprecation import MiddlewareMixin

from lib.http import render_json
from common import errors
from user.models import User
from common.errors import LogicErr


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 白名单, 在白名单内的地址就直接返回
        white_list = ['/api/user/submit/phone/', '/api/user/submit/vcode/']
        if request.path in white_list:
            return None
        # 判断request的session中是否存在uid, 如果存在, 则说明已经登录
        # 不存在就没登录, 就提示没登录
        uid = request.session.get('uid')
        if not uid:
            return render_json(code=errors.LOGIN_REQUIRED, data='请登录')
        # 如果登录了, 就把user写入request
        user = User.objects.get(id=uid)
        request.user = user


class LogicErrMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        # 只捕获逻辑错误
        if isinstance(exception, LogicErr):
            return render_json(exception.code, exception.data)
        return None
