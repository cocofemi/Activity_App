# Generated by Django 2.2.3 on 2019-10-17 09:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0010_bookmarkactivity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookmarkactivity',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]