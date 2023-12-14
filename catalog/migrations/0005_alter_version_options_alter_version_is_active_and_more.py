# Generated by Django 4.2.7 on 2023-12-14 03:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_version'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='version',
            options={'ordering': ('version_number',), 'verbose_name': 'Версия', 'verbose_name_plural': 'Версии'},
        ),
        migrations.AlterField(
            model_name='version',
            name='is_active',
            field=models.BooleanField(choices=[(True, 'активная'), (False, 'не активная')], verbose_name='Статус версии'),
        ),
        migrations.AlterField(
            model_name='version',
            name='version_number',
            field=models.IntegerField(blank=True, default=1, verbose_name='Номер версии'),
        ),
    ]