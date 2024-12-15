# Generated by Django 5.1.2 on 2024-12-15 21:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_colaborador_equipe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colaborador',
            name='cargo',
            field=models.CharField(max_length=200, verbose_name='Cargo'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='centro_custo',
            field=models.CharField(default='MUSASHI - MANAUS', max_length=100, verbose_name='Centro de Custo'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='turno',
            field=models.CharField(choices=[('1T', 'MUSASHI - 1 TURNO - 07:00 as 15:05 - Segunda-Feira à Sábado'), ('2T', 'MUSASHI - 2 TURNO - 14:50 as 22:48 - Segunda-Feira à Sábado'), ('RD', 'REVEZAMENTO 1 (DIURNO) - 07:00 as 19:00 (1x1)'), ('RN', 'REVEZAMENTO 2 (NOTURNO) - 19:00 as 07:00 (1x1)')], max_length=200, verbose_name='Turno'),
        ),
    ]
