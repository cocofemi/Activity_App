# Generated by Django 2.2.3 on 2019-11-02 22:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0013_auto_20191022_0129'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='target',
        ),
    ]