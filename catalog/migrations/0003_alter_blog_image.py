# Generated by Django 4.2.7 on 2023-12-03 11:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0002_blog'),
    ]

    operations = [
        migrations.AlterField(
            model_name='blog',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='products/', verbose_name='Изображение'),
        ),
    ]