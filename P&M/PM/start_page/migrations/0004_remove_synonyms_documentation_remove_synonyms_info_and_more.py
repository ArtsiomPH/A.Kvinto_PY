# Generated by Django 4.0 on 2022-04-04 12:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('start_page', '0003_alter_medcine_pub_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='synonyms',
            name='documentation',
        ),
        migrations.RemoveField(
            model_name='synonyms',
            name='info',
        ),
        migrations.RemoveField(
            model_name='synonyms',
            name='sources',
        ),
        migrations.AddField(
            model_name='medcine',
            name='general_url_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Название для URL'),
        ),
        migrations.AddField(
            model_name='synonyms',
            name='url_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Название для URL'),
        ),
        migrations.AlterField(
            model_name='medcine',
            name='general_documentation',
            field=models.URLField(blank=True, null=True, verbose_name='Ссылка на документацию'),
        ),
        migrations.AlterField(
            model_name='medcine',
            name='general_info',
            field=models.TextField(blank=True, null=True, verbose_name='Информация'),
        ),
        migrations.AlterField(
            model_name='medcine',
            name='general_sources',
            field=models.TextField(blank=True, null=True, verbose_name='Литература'),
        ),
        migrations.AlterField(
            model_name='medcine',
            name='international_name',
            field=models.CharField(max_length=300, verbose_name='МНН'),
        ),
        migrations.AlterField(
            model_name='synonyms',
            name='comm_name',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Торговое наименование'),
        ),
        migrations.AlterField(
            model_name='synonyms',
            name='medcine',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='start_page.medcine', verbose_name='Международное наименование'),
        ),
        migrations.AlterField(
            model_name='synonyms',
            name='pub_date',
            field=models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Дата публикации'),
        ),
    ]