# Generated by Django 2.2.3 on 2019-09-09 10:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0004_auto_20190909_1521'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='num',
            field=models.IntegerField(default=1),
        ),
    ]
