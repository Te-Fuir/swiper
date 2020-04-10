from lib.http import render_json
from social import logic


def get_recd_list(request):
    """获取用户列表"""
    # 注意事项: 1. 已经滑过的人,不应该再出现.
    # 2. 自己也不能出现在推荐列表.
    # 3. 只推荐符合自己交友资料的用户.
    user = request.user
    data = logic.get_recd_list(user)
    return render_json(data=data)


def like(request):
    user = request.user
    sid = int(request.POST.get('sid'))
    flag = logic.like(user.id, sid)
    return render_json(data={'match': flag})


def dislike(request):
    user = request.user
    print(request.POST.get('sid'))
    sid = int(request.POST.get('sid'))
    flag = logic.dislike(user.id, sid)
    return render_json(data={'unmatch': flag})


def superlike(request):
    user = request.user
    sid = int(request.POST.get('sid'))
    flag = logic.superlike(user.id, sid)
    return render_json(data={'match': flag})


def rewind(request):
    """
    每天允许反悔3次, 把已经反悔的次数记录在redis中
    每次执行反悔操作之前, 先判断反悔次数是否小于配置的当天最大反悔次数
    """
    # 先从缓存中获取当天已经反悔的次数
    user = request.user
    code, data = logic.rewind(user)
    return render_json(code, data)


def show_friends_list(request):
    """查看好友列表"""
    user = request.user
    data = logic.show_friends_list(user)
    return render_json(data=data)


def show_friend_information(request):
    """查看好友信息"""
    sid = request.POST.get('sid')
    data = logic.show_friend_information(sid=sid)
    return render_json(data=data)
