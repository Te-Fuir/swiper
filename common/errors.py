SMS_ERROR = 1000
VCODE_ERROR = 1001
LOGIN_REQUIRED = 1002
PROFILE_ERROR = 1003
EXCEED_MAXIMUM_REWIND = 1004
NO_RECORD = 1005


class LogicErr(Exception):
    code = None
    data = None


# 定义一个生成异常类的工厂方法
def gen_logic_err(name, code, data):
    return type(name, (LogicErr,), {'code': code, 'data': data})


SmsError = gen_logic_err('SmsError', code=1000, data='短信发送失败')
VcodeError = gen_logic_err('VcodeError', code=1001, data='验证码错误')
LoginRequiredError = gen_logic_err('LoginRequiredError', code=1002, data='请登录')
ProfileError = gen_logic_err('ProfileError', code=1003, data='个人交友资料数据不合法')
ExceedMaximumRewindError = gen_logic_err('ExceedMaximumRewindError', code=1004, data='超出今日反悔次数')
NoRecordError = gen_logic_err('NoRecordError', code=1005, data='没有记录, 无法反悔')
