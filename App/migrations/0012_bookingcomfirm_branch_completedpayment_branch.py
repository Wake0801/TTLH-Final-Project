# Generated by Django 4.2.6 on 2023-12-30 15:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0011_branch'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookingcomfirm',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='App.branch'),
        ),
        migrations.AddField(
            model_name='completedpayment',
            name='branch',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='App.branch'),
        ),
    ]
