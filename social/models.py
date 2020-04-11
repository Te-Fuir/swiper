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

    @classmethod
    def like(cls, uid, sid):
        return cls.objects.create(uid=uid, sid=sid, mark='like')

    @classmethod
    def dislike(cls, uid, sid):
        return cls.objects.create(uid=uid, sid=sid, mark='dislike')

    @classmethod
    def superlike(cls, uid, sid):
        return cls.objects.create(uid=uid, sid=sid, mark='superlike')

    @classmethod
    def has_like(cls, uid, sid):
        return cls.objects.filter(uid=uid, sid=sid).exists()


class Friend(models.Model):
    uid1 = models.IntegerField()
    uid2 = models.IntegerField()

    @classmethod
    def make_friends(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        friendship = cls.objects.create(uid1=uid1, uid2=uid2)
        return friendship

    @classmethod
    def is_friend(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        return cls.objects.filter(uid1=uid1, uid2=uid2).exists()

    @classmethod
    def delete_friend(cls, uid1, uid2):
        uid1, uid2 = (uid1, uid2) if uid1 < uid2 else (uid2, uid1)
        return cls.objects.filter(uid1=uid1, uid2=uid2).delete()
