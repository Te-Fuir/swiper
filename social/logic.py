import datetime

from social.models import Swiped
from user.models import User


def get_recd_list(user):
    # 根据最大和最小的交友年龄
    now = datetime.datetime.now()
    max_birth_year = now.year - user.profile.min_dating_age
    min_birth_year = now.year - user.profile.max_dating_age

    # 查询已经被当前用户滑过的人
    swiped_list = Swiped.objects.filter(uid=user.id).only('sid')
    # 取出sid
    sid_list = [s.sid for s in swiped_list]
    sid_list.append(user.id)

    users = User.objects.filter(
        location=user.profile.location,
        birth_year__range=[min_birth_year, max_birth_year],
        sex=user.profile.dating_sex
    ).exclude(id__in=sid_list)[:20]
    data = [user.to_dict() for user in users]
    return data
