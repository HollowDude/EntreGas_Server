# Generated by Django 5.1.7 on 2025-03-20 03:17

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Trabajador',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('correo', models.EmailField(max_length=254)),
                ('puesto', models.CharField(choices=[('tecnico', 'Tecnico'), ('jefe de servicio', 'Jefe de Servicio')], max_length=255)),
            ],
        ),
    ]
