# Generated by Django 3.1.1 on 2020-10-14 09:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trips', '0004_auto_20200929_2209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='from_user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer', to='accounts.user'),
        ),
    ]
