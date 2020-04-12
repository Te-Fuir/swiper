import datetime

from django.core.cache import cache
from django.db.models import Q

from common import keys, errors
from lib.cache import rds
from lib.http import render_json
from social.models import Swiped, Friend
from swiper import config
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


def like(uid, sid):
    # 创建一条记录
    Swiped.like(uid, sid)
    # 判断对方是否喜欢我们, 是就建立好友关系
    if Swiped.has_like(uid=sid, sid=uid):
        Friend.make_friends(uid1=uid, uid2=sid)
        return True
    return False


def dislike(uid, sid):
    Swiped.dislike(uid, sid)
    Friend.delete_friend(uid, sid)
    return True


def superlike(uid, sid):
    # 创建一条记录
    Swiped.superlike(uid, sid)
    # 判断对方是否喜欢我们, 是就建立好友关系
    if Swiped.has_like(uid=sid, sid=uid):
        Friend.make_friends(uid1=uid, uid2=sid)
        return True
    return False


def rewind(user):
    key = keys.REWIND_KEY % user.id
    cache_rewinded_times = cache.get(key, 0)
    if cache_rewinded_times < config.MAX_REWIND:
        # 说明当天还有反悔次数, 反悔次数每次都要加1
        cache_rewinded_times += 1
        now = datetime.datetime.now()
        left_seconds = 86400 - (now.hour * 3600 + now.minute * 60 + now.second)
        cache.set(key, cache_rewinded_times, timeout=left_seconds)
        # 删除Swiped表中最近的的一条记录
        try:
            record = Swiped.objects.filter(uid=user.id).latest('time')
            # 考虑如果有好友关系, 反悔之后好友关系也解除
            Friend.delete_friend(uid1=user.id, uid2=record.sid)
            record.delete()
            return 0, None
        except Swiped.DoesNotExist:
            raise errors.NoRecordError

    else:
        raise errors.ExceedMaximumRewindError


def show_friends_list(user):
    friends = Friend.objects.filter(Q(uid1=user.id) | Q(uid2=user.id))
    # 把好友的id取出来
    friends_id = []
    for friend in friends:
        if friend.uid1 == user.id:
            friends_id.append(friend.uid2)
        else:
            friends_id.append(friend.uid1)
    users = User.objects.filter(id__in=friends_id)
    data = [user.to_dict() for user in users]
    return data


def show_friend_information(sid):
    users = User.objects.get(id=sid)
    data = users.to_dict()
    return data


def get_top_n():
    # 取出redis中的得分排行
    score_list = rds.zrevrange('Hot-Rank', 0, config.TOP_N, withscore=True)
    cleaned_data = [(int(uid), score) for uid, score in score_list]
    uid_list = [uid for uid, _ in cleaned_data]
    users = User.objects.filter(id__in=uid_list)
    # 对users进行排序
    users = sorted(users, key=lambda user: uid_list.index(user.id))
    # 生成数据
    data = []
    for rank, (_, score), user in zip(range(1, config.TOP_N + 1), cleaned_data, users):
        temp = {}
        temp['rank'] = rank
        temp['score'] = score
        temp.update(user.to_dict())
        data.append(temp)
    return data
