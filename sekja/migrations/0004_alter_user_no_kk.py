# Generated by Django 3.2.9 on 2021-12-04 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sekja', '0003_alter_user_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='no_KK',
            field=models.IntegerField(max_length=16, unique=True),
        ),
    ]
