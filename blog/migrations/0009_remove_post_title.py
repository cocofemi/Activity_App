# Generated by Django 2.2.3 on 2019-12-18 21:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_post_likes'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='title',
        ),
    ]