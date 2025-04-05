from django.db import models


class BaseModel(models.Model):
    name = models.CharField(max_length=255, default="", verbose_name="名称")
    order = models.IntegerField(default=0, verbose_name="序号")
    is_active = models.BooleanField(default=True, verbose_name="是否使用")
    is_display = models.BooleanField(default=True, verbose_name="是否显示")
    # 自动设置为当前时间
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    # 每次保存后自动设置为当前时间
    update_time = models.DateTimeField(auto_now=True, )

    class Meta:
        abstract = True
