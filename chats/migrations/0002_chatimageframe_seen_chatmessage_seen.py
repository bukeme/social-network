# Generated by Django 4.2.1 on 2023-06-19 04:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatimageframe',
            name='seen',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='chatmessage',
            name='seen',
            field=models.BooleanField(default=False),
        ),
    ]