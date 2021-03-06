# Generated by Django 2.1.2 on 2018-10-12 21:39

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('vms', '0002_staffingagency'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True, help_text='A boolean indicating if this user is currently active. Inactive employees log any working hours.', verbose_name='is active')),
                ('time_created', models.DateTimeField(auto_now_add=True, help_text='The time the employee was created.', verbose_name='time created')),
                ('time_updated', models.DateTimeField(auto_now=True, help_text='The time the employee was last updated.', verbose_name='time updated')),
                ('staffing_agency', models.ForeignKey(help_text='The staffing agency that hired the employee.', on_delete=django.db.models.deletion.CASCADE, related_name='employees', related_query_name='employee', to='vms.StaffingAgency', verbose_name='staffing agency')),
                ('supervisor', models.ForeignKey(help_text="The client administrator who can approve the user's hours.", null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='employees', related_query_name='employee', to='vms.ClientAdmin', verbose_name='supervisor')),
                ('user', models.ForeignKey(help_text='The user account the employee is attached to.', on_delete=django.db.models.deletion.CASCADE, related_name='employees', related_query_name='employee', to=settings.AUTH_USER_MODEL, verbose_name='user')),
            ],
            options={
                'verbose_name': 'employee',
                'verbose_name_plural': 'employees',
                'ordering': ('time_created',),
            },
        ),
    ]
