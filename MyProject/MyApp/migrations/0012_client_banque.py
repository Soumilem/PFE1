# Generated by Django 4.2.1 on 2023-06-15 14:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('MyApp', '0011_client_nni'),
    ]

    operations = [
        migrations.CreateModel(
            name='client_banque',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('NNI', models.DecimalField(decimal_places=0, max_digits=10)),
                ('num_compte', models.CharField(max_length=10, unique=True)),
                ('banque', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='client_banque', to='MyApp.banque')),
            ],
        ),
    ]
