# Generated by Django 4.2.20 on 2025-06-09 16:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0015_rename_trabajador_recivio_comprobante_abastecimiento_trabajador_recibio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reporte_devolucion',
            name='cilindro',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='app.cilindro'),
        ),
    ]
