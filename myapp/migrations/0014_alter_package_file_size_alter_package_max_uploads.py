# Generated by Django 5.0.2 on 2024-04-06 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0013_delete_testpackage_package_file_size_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='package',
            name='file_size',
            field=models.BigIntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='package',
            name='max_uploads',
            field=models.IntegerField(blank=True),
        ),
    ]
