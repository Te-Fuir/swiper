from django.db import models


class Vip(models.Model):
    level = models.IntegerField(default=0, verbose_name='vip等级')
    price = models.FloatField(verbose_name='vip价格')
    name = models.CharField(max_length=128, verbose_name='vip名称')

    def __str__(self):
        return f'<Vip {self.level}>'


class Permission(models.Model):
    name = models.CharField(max_length=128, verbose_name='权限名称')
    description = models.TextField(verbose_name='权限描述')

    def __str__(self):
        return f'<Perm {self.name}>'


class VipPermRelation(models.Model):
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()
