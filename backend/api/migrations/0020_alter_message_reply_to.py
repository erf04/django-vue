# Generated by Django 4.2.5 on 2024-03-15 23:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_alter_groupadmin_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='reply_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='api.message'),
        ),
    ]
