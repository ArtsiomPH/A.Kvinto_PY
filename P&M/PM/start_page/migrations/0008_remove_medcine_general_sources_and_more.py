# Generated by Django 4.0 on 2022-04-06 20:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('start_page', '0007_general_sources_remove_medcine_general_sources_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='medcine',
            name='general_sources',
        ),
        migrations.AddField(
            model_name='general_sources',
            name='medcine',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='start_page.medcine', verbose_name='МНН'),
        ),
    ]