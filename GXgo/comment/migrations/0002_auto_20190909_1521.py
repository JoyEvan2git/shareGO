# Generated by Django 2.2.3 on 2019-09-09 07:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comment', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ('created',), 'verbose_name': '评论', 'verbose_name_plural': '评论类'},
        ),
    ]
