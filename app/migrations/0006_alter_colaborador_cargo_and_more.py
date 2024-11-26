# Generated by Django 5.1.2 on 2024-11-26 11:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_colaborador_cargo_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='colaborador',
            name='cargo',
            field=models.CharField(max_length=100, verbose_name='Cargo'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='centro_custo',
            field=models.CharField(max_length=100, verbose_name='Centro de Custo'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='cpf',
            field=models.CharField(blank=True, max_length=14, null=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='data_admissao',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Admissão'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='data_demissao',
            field=models.DateField(blank=True, null=True, verbose_name='Data de Demissão'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='matricula',
            field=models.CharField(max_length=20, unique=True, verbose_name='Matrícula'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='nome',
            field=models.CharField(max_length=200, verbose_name='Nome'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='pis',
            field=models.CharField(blank=True, max_length=14, null=True, verbose_name='PIS'),
        ),
        migrations.AlterField(
            model_name='colaborador',
            name='turno',
            field=models.CharField(max_length=100, verbose_name='Turno'),
        ),
        migrations.CreateModel(
            name='PontoForm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('arquivo', models.FileField(upload_to='pontos/')),
                ('data_envio', models.DateTimeField(auto_now_add=True)),
                ('colaborador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pontos', to='app.colaborador')),
            ],
        ),
    ]
