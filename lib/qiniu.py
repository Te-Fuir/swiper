from qiniu import Auth, put_file, etag

from swiper import config
from common import keys


def upload_qiniu(user, file_path):
    # 构建鉴权对象
    q = Auth(config.QN_AK, config.QN_SK)
    # 要上传的空间
    bucket_name = 'sz1906'
    filename = keys.AVATAR_KEY % user.id
    # 生成上传 Token，可以指定过期时间等
    token = q.upload_token(bucket_name, filename, 3600)
    ret, info = put_file(token, filename, file_path)
