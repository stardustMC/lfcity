from home.models import Nav
from django.core.management.base import BaseCommand

class Command(BaseCommand):

    def handle(self, *args, **options):
        header = ['免费课', '项目课', '学位课', '习题库']
        header_urls = ['/free', '/project', '/degree', '/exam']
        for i in range(len(header)):
            Nav.objects.create(
                name=header[i],
                link=header_urls[i],
                position=0
            )

        footer = ['路飞学城', '企业服务', '关于我们', '联系我们', '商业合作', '帮助中心', '意见反馈', '新手指南']
        for i in range(len(footer)):
            Nav.objects.create(
                name=footer[i],
                # 尚未开发，先测试使用
                link="/free",
                position=1
            )