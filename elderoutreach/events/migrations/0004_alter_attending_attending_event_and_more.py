# Generated by Django 4.0.7 on 2022-10-19 00:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('events', '0003_attending_att_id_alter_attending_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attending',
            name='attending_event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attending_event', to='events.events'),
        ),
        migrations.AlterField(
            model_name='attending',
            name='attending_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='attending_user', to=settings.AUTH_USER_MODEL),
        ),
    ]
