from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):

    phone = models.CharField(max_length=11, unique=True, null=True, blank=True, verbose_name="手机号码")
    nickname = models.CharField(max_length=20, default="小白", verbose_name="昵称")
    balance = models.FloatField(default=0.0, verbose_name="余额", help_text="账户余额，可购买课程")
    credits = models.IntegerField(default=0, verbose_name="积分", help_text="账户积分，可抵扣价格")
    avatar = models.ImageField(upload_to="avatar/%Y", default="", null=True, verbose_name="个人头像")

    class Meta:
        db_table = "lf_user"
        verbose_name = "用户"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username