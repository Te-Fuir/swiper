import random
import requests
from django.core.cache import cache
from swiper import config
from common import keys


def gen_vcode(size=4):
    start = 10 ** (size - 1)
    end = 10 ** size - 1
    return str(random.randint(start, end))


def send_sms(phone):
    params = config.YZX_PARAMS.copy()
    params['mobile'] = phone
    vcode = gen_vcode()
    cache.set(keys.VCODE_KEY % phone, vcode, timeout=600)
    params['param'] = vcode
    resp = requests.post(config.YZX_URL, json=params)

    if resp.status_code == 200:
        # 说明访问短信服务器没问题
        result = resp.json()
        if result['code'] == '000000':
            return True, 'ok'
        else:
            return False, result['msg']
    else:
        return False, '访问短信服务器有误'
