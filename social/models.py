from django.db import models


class Swiped(models.Model):
    MARK = (
        ('like', 'like'),
        ('dislike', 'dislike'),
        ('superlike', 'superlike')
    )
    uid = models.IntegerField(verbose_name='用户自身id')
    sid = models.IntegerField(verbose_name='被滑的陌生人id')
    mark = models.CharField(max_length=16, choices=MARK, verbose_name='滑动类型')
    time = models.DateTimeField(auto_now_add=True, verbose_name='滑动的时间')

