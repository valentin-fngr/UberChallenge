# Generated by Django 3.1.1 on 2020-09-29 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0003_auto_20200927_1122'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='status',
            field=models.CharField(choices=[('COMPLETED', 'COMPLETED'), ('IN_PROGRESS', 'IN_PROGRESS'), ('REQUESTED', 'REQUESTED'), ('ACCEPTED', 'ACCEPTED')], default='REQUESTED', max_length=20),
        ),
    ]
