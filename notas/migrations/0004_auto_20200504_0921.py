# Generated by Django 3.0.5 on 2020-05-04 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notas', '0003_auto_20200504_0727'),
    ]

    operations = [
        migrations.AlterField(
            model_name='nota',
            name='controles',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nota',
            name='examen_final',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nota',
            name='practicos',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nota',
            name='primer_parcial',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='nota',
            name='segundo_parcial',
            field=models.IntegerField(null=True),
        ),
    ]
