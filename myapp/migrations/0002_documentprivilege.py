# Generated by Django 5.0.2 on 2024-03-15 11:15

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Documentprivilege',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('privilege_status', models.CharField(choices=[('draft', 'Draft'), ('granted', 'Granted'), ('revoked', 'Revoked')], max_length=60)),
                ('docid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.document')),
                ('sent_to', models.ManyToManyField(related_name='received_documents', to='myapp.login')),
                ('userid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.login')),
            ],
        ),
    ]
