# Generated by Django 4.1.7 on 2023-03-30 13:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('DashBoard', '0005_alter_profile_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='user',
            field=models.IntegerField(default=1),
        ),
    ]