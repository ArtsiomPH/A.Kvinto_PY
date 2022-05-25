# Generated by Django 4.0 on 2022-05-24 15:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('start_page', '0013_alter_medcine_formula'),
    ]

    operations = [
        migrations.AlterField(
            model_name='general_sources',
            name='medcine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='start_page.medcine', verbose_name='МНН'),
        ),
        migrations.AlterField(
            model_name='synonyms',
            name='medcine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='start_page.medcine', verbose_name='Международное наименование'),
        ),
    ]