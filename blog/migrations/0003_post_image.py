# Generated by Django 2.2.3 on 2019-09-11 22:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_post_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='image',
            field=models.ImageField(null=True, upload_to='post_pics'),
        ),
    ]
