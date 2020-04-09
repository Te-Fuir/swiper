import datetime

from user.models import User


def get_recd_list(request):
    """获取推荐列表"""
    user = request.user
    now = datetime.datetime.now()
    max_birth_year = now.year - user.profile.min_dating_age
    min_birth_year = now.year - user.profile.max_dating_age
    User.objects.filter(
        location=user.profile.location
    )
