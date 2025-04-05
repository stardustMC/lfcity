from django.db import models
from models import BaseModel


# Create your models here.
class Nav(BaseModel):
    """导航栏"""
    pos_choices = (
        (0, "顶部"),
        (1, "底部")
    )
    link = models.CharField(default='', max_length=200, verbose_name='链接')
    is_http = models.BooleanField(default=False, verbose_name="是否是外部链接")
    position = models.IntegerField(choices=pos_choices, default=0, verbose_name="导航位置")

    class Meta:
        db_table = 'lf_nav'
        verbose_name = "导航菜单"
        verbose_name_plural = verbose_name

class Banner(BaseModel):
    """轮播图"""
    image = models.ImageField(verbose_name="轮播图片", upload_to='banner/%Y/')
    link = models.CharField(verbose_name="链接地址", max_length=200, default='')
    is_http = models.BooleanField(verbose_name="是否是外部链接", default=False)

    class Meta:
        db_table = 'lf_banner'
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name