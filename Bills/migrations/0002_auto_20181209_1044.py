# Generated by Django 2.1.3 on 2018-12-09 10:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Bills', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill',
            name='group',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BillGroups.BillGroups'),
        ),
    ]
