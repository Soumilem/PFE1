# Generated by Django 4.2.1 on 2023-06-12 09:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0006_rename_user_banque_responsable_banque'),
    ]

    operations = [
        migrations.RenameField(
            model_name='banque',
            old_name='responsable_banque',
            new_name='user',
        ),
    ]