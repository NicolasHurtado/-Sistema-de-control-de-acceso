# Generated by Django 3.2.14 on 2022-08-21 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ControlAcceso', '0005_auto_20220821_0106'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='estado',
            field=models.BooleanField(default=False),
        ),
    ]
