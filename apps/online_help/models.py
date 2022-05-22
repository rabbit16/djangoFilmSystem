from django.db import models
from django.utils import timezone
from django.contrib.auth.models import UserManager as _UserManager, AbstractUser

class Problems(models.Model):
    Problems_id = models.CharField(max_length=20,help_text="问题id",verbose_name="问题id")

    class Meta:
        db_table = 'tb_Problems'
        verbose_name = '问题咨询'
# Create your models here.
