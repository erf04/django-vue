# Generated by Django 4.2.5 on 2024-03-15 23:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_alter_message_reply_to'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.message'),
        ),
    ]
