# Generated by Django 2.2.3 on 2019-09-13 09:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0005_auto_20190913_0854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='slug',
            field=models.SlugField(null=True, unique=True),
        ),
    ]