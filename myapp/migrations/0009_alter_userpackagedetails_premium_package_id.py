# Generated by Django 5.0.2 on 2024-04-04 21:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_alter_testpackage_file_size'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userpackagedetails',
            name='premium_package_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.testpackage'),
        ),
    ]
