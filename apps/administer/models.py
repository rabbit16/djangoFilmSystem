from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager as _UserManager, AbstractUser


class Carousel_figure(models.Model):
    Figure_id = models.CharField(max_length=20, help_text="轮播图id", verbose_name="轮播图id")
    Figure_img = models.CharField(max_length=100, verbose_name="轮播图图片", help_text="轮播图图片")

    class Meta:
        db_table = 'tb_Figure'
        verbose_name = '轮播图'

    def __str__(self):
        return self.Figure_id