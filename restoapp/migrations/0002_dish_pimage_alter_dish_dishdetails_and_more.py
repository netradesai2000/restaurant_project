# Generated by Django 5.0 on 2023-12-18 03:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restoapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dish',
            name='pimage',
            field=models.ImageField(default=0, upload_to='image'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='dish',
            name='dishdetails',
            field=models.CharField(max_length=100, verbose_name='Dish details'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='Availabel'),
        ),
        migrations.AlterField(
            model_name='dish',
            name='name',
            field=models.CharField(max_length=50, verbose_name='Dish name'),
        ),
    ]
