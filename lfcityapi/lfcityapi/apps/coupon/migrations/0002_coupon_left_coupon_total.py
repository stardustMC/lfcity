# Generated by Django 4.2.17 on 2025-04-05 12:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coupon', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='coupon',
            name='left',
            field=models.IntegerField(blank=True, default=100, verbose_name='剩余数量'),
        ),
        migrations.AddField(
            model_name='coupon',
            name='total',
            field=models.IntegerField(blank=True, default=100, verbose_name='发放数量'),
        ),
    ]
