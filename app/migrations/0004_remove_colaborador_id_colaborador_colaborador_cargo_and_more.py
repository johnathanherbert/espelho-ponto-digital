# Generated by Django 5.1.2 on 2024-11-26 10:19

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_siteconfiguration'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='colaborador',
            name='id_colaborador',
        ),
        migrations.AddField(
            model_name='colaborador',
            name='cargo',
            field=models.CharField(default='Não especificado', max_length=100, verbose_name='Cargo'),
        ),
        migrations.AddField(
            model_name='colaborador',
            name='centro_custo',
            field=models.CharField(default='Não especificado', max_length=100, verbose_name='Centro de Custo'),
        ),
        migrations.AddField(
            model_name='colaborador',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True, validators=[django.core.validators.RegexValidator(message='CPF deve estar no formato XXX.XXX.XXX-XX', regex='^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$')], verbose_name='CPF'),
        ),
        migrations.AddField(
            model_name='colaborador',
            name='data_demissao',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Demissão'),
        ),
        migrations.AddField(
            model_name='colaborador',
            name='matricula',
            field=models.CharField(blank=True, max_length=10, null=True, unique=True, verbose_name='Matrícula'),
        ),
        migrations.AddField(
            model_name='colaborador',
            name='pis',
            field=models.CharField(blank=True, max_length=14, null=True, validators=[django.core.validators.RegexValidator(message='PIS deve estar no formato XXX.XXXXX.XX-X', regex='^\\d{3}\\.\\d{5}\\.\\d{2}-\\d{1}$')], verbose_name='PIS'),
        ),
        migrations.AddField(
            model_name='colaborador',
            name='turno',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Turno'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='nome',
            field=models.CharField(max_length=200, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='background_color',
            field=models.CharField(default='#F3F4F6', max_length=7, validators=[django.core.validators.RegexValidator(message='Digite uma cor hexadecimal válida (ex: #FF0000)', regex='^#([A-Fa-f0-9]{6})$')], verbose_name='Cor de Fundo'),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='link_color',
            field=models.CharField(default='#2563EB', max_length=7, validators=[django.core.validators.RegexValidator(message='Digite uma cor hexadecimal válida (ex: #FF0000)', regex='^#([A-Fa-f0-9]{6})$')], verbose_name='Cor dos Links'),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='primary_color',
            field=models.CharField(default='#3B82F6', max_length=7, validators=[django.core.validators.RegexValidator(message='Digite uma cor hexadecimal válida (ex: #FF0000)', regex='^#([A-Fa-f0-9]{6})$')], verbose_name='Cor Primária'),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='secondary_color',
            field=models.CharField(default='#1D4ED8', max_length=7, validators=[django.core.validators.RegexValidator(message='Digite uma cor hexadecimal válida (ex: #FF0000)', regex='^#([A-Fa-f0-9]{6})$')], verbose_name='Cor Secundária'),
        ),
        migrations.AlterField(
            model_name='siteconfiguration',
            name='text_color',
            field=models.CharField(default='#111827', max_length=7, validators=[django.core.validators.RegexValidator(message='Digite uma cor hexadecimal válida (ex: #FF0000)', regex='^#([A-Fa-f0-9]{6})$')], verbose_name='Cor do Texto'),
        ),
    ]
