from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager as _UserManager, AbstractUser


class Problems_type(models.Model):  # 问题标签
    type_id = models.IntegerField(verbose_name="标签序号", help_text="标签序号")
    type_name = models.CharField(max_length=20, help_text="问题标签", verbose_name="问题标签")

    class Meta:
        db_table = "tb_movie_type"
        verbose_name = "问题标签"

    def __str__(self):
        return self.type_name

class Problems(models.Model):
    Problems_id = models.CharField(max_length=20,help_text="问题id",verbose_name="问题id")
    Problems_contain = models.CharField(max_length=1000, help_text="问题内容", verbose_name="问题内容")
    p_problemtype = models.ManyToManyField(Problems_type)
    class Meta:
        db_table = 'tb_Problems'
        verbose_name = '问题咨询'
    def __str__(self):
        return self.Problems_id

