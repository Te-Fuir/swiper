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
