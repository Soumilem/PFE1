# Generated by Django 4.2.1 on 2023-06-15 12:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0010_delete_client_nni'),
    ]

    operations = [
        migrations.CreateModel(
            name='client_nni',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NNI', models.DecimalField(decimal_places=0, max_digits=10, unique=True)),
            ],
        ),
    ]
