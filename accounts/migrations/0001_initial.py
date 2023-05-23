# Generated by Django 4.2.1 on 2023-05-19 12:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('other_name', models.CharField(blank=True, max_length=200, null=True)),
                ('birth_date', models.DateField(blank=True, null=True)),
                ('phone', models.CharField(blank=True, max_length=50, null=True)),
                ('occupation', models.CharField(blank=True, max_length=200, null=True)),
                ('location', models.CharField(blank=True, max_length=250, null=True)),
                ('overview', models.TextField(blank=True, null=True)),
                ('marital_status', models.CharField(blank=True, max_length=100, null=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='ProfileImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_image', models.ImageField(default='profile_images/placeholder.jpg', upload_to='profile_images/%Y-%m-%d/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('userprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
        migrations.CreateModel(
            name='CoverImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cover_image', models.ImageField(default='cover_images/placeholder.jpg', upload_to='cover_images/%Y-%m-%d/')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('userprofile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.userprofile')),
            ],
            options={
                'ordering': ('-created',),
            },
        ),
    ]
