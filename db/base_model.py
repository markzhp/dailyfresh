"""
模型基类
抽象类
用于被继承
减少代码重复
"""

from django.db import models


class BaseModel(models.Model):
    """
    模型抽象基类
    增加插入时间、更新时间和逻辑删除标志
    """
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    update_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_delete = models.BooleanField(default=False, verbose_name='逻辑删除')

    class Meta:
        abstract = True
