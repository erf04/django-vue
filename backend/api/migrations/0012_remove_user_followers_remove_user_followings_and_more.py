# Generated by Django 4.2.5 on 2024-03-09 08:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_remove_user_channel_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='followers',
        ),
        migrations.RemoveField(
            model_name='user',
            name='followings',
        ),
        migrations.CreateModel(
            name='Follower',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('followed', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followers', to=settings.AUTH_USER_MODEL)),
                ('follower', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='followings', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('follower', 'followed')},
            },
        ),
    ]
