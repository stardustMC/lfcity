from django.db import models
from django.contrib.auth.models import AbstractUser

from models import BaseModel


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

class Credit(BaseModel):
    """积分流水"""
    opera_choices = (
        (0, "业务增值"),
        (1, "购物消费"),
        (2, "系统赠送"),
    )
    operation = models.SmallIntegerField(choices=opera_choices, default=1, verbose_name="积分操作类型")
    number = models.IntegerField(default=0, verbose_name="积分数量", help_text="扣除积分需要设置为负数<br>添加积分需要设置为正数")
    user = models.ForeignKey(User, related_name='user_credits', on_delete=models.CASCADE, db_constraint=False, verbose_name="用户")
    # remark = models.CharField(max_length=500, null=True, blank=True, verbose_name="备注信息")

    class Meta:
        db_table = 'lf_credit'
        verbose_name = '积分流水'
        verbose_name_plural = verbose_name

    def __str__(self):
        if self.number > 0:
            oper_text = "获得"
        else:
            oper_text = "减少"
        return "[%s] %s 用户%s %s %s积分" % (self.get_operation_display(),self.create_time.strftime("%Y-%m-%d %H:%M:%S"), self.user.username, oper_text, abs(self.number))