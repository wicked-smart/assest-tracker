# Generated by Django 4.2.9 on 2024-01-31 10:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('asset_tracker', '0003_alter_user_employee_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='alloted_to',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assets_allocated', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='asset',
            name='current_allocation_status',
            field=models.CharField(choices=[('ALLOCATED', 'Allocated'), ('UNALLOCATED', 'Unallocated')], default='UNALLOCATED', max_length=15),
        ),
    ]
