# Generated by Django 2.1.3 on 2018-12-05 15:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='pin',
            field=models.CharField(blank=True, default='None', max_length=4, null=True),
        ),
    ]
