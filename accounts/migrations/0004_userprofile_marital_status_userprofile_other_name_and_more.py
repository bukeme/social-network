# Generated by Django 4.2.1 on 2023-05-07 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_coverimage_options_alter_profileimage_options_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='marital_status',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='other_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='overview',
            field=models.TextField(blank=True, null=True),
        ),
    ]
