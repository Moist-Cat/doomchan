# Generated by Django 3.1.7 on 2021-07-17 01:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageboard', '0003_auto_20210717_0156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='comment',
            field=models.TextField(blank=True, help_text='Comment. 2K chars.', max_length=2000),
        ),
        migrations.AlterField(
            model_name='comment',
            name='image',
            field=models.ImageField(upload_to='images/<property object at 0x7f94cc695950>/'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='name',
            field=models.CharField(blank=True, default='Anonymous', help_text='User name. 14 chars', max_length=14),
        ),
        migrations.AlterField(
            model_name='thread',
            name='image',
            field=models.ImageField(upload_to='images/<django.db.models.query_utils.DeferredAttribute object at 0x7f94cc08fe20>/'),
        ),
    ]