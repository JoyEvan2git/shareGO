# Generated by Django 2.2.3 on 2019-09-09 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_auto_20190829_2101'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户类'},
        ),
    ]