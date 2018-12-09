# Generated by Django 2.1.3 on 2018-12-09 05:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=2048)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='auth.Group')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('state', models.CharField(choices=[('PR', 'Prepare'), ('AP', 'Approved'), ('RJ', 'Recected'), ('CS', 'Concencus'), ('CD', 'Commited'), ('FN', 'Finish'), ('SP', 'Suspend')], default='PR', max_length=2)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bills.Bill')),
                ('from_u', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='from_u', to=settings.AUTH_USER_MODEL)),
                ('to_u', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='to_u', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
