# Generated by Django 2.2.3 on 2019-10-02 22:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('activity', '0005_auto_20190917_2133'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='category',
            field=models.CharField(choices=[('A', 'Arts'), ('A', 'Adventure'), ('B', 'Business'), ('D', 'Design'), ('E', 'Entertainment'), ('ED', 'Education'), ('H', 'Health'), ('FT', 'Fitness'), ('FA', 'Fashion'), ('FD', 'Food'), ('M', 'Music'), ('P', 'Programming'), ('S', 'Startup'), ('T', 'Technology'), ('O', 'Other')], max_length=100, null=True),
        ),
    ]
