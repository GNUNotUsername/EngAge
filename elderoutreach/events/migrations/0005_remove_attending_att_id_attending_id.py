# Generated by Django 4.0.7 on 2022-10-19 00:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0004_alter_attending_attending_event_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='attending',
            name='att_id',
        ),
        migrations.AddField(
            model_name='attending',
            name='id',
            field=models.BigAutoField(auto_created=True, default=1, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
    ]
