# Generated by Django 4.0.1 on 2022-01-15 14:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0002_profiledata_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='uniquecode',
            new_name='usercode',
        ),
    ]