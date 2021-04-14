# Generated by Django 2.2.3 on 2019-09-13 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0004_comment_parent'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='image',
            field=models.ImageField(null=True, upload_to='post_pics'),
        ),
        migrations.AddField(
            model_name='comment',
            name='slug',
            field=models.SlugField(max_length=30, null=True, unique=True),
        ),
    ]
