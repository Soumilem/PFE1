# Generated by Django 4.2.1 on 2023-06-12 09:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0007_rename_responsable_banque_banque_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banque',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
