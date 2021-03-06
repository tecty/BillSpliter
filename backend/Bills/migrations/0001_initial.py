# Generated by Django 2.1.7 on 2019-02-14 16:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('BillGroups', '0001_initial'),
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
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BillGroups.BillGroups')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Settlement',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('title', models.CharField(max_length=255)),
                ('description', models.CharField(blank=True, max_length=2048)),
                ('wait_count', models.PositiveIntegerField(default=1)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='BillGroups.BillGroups')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SettleTransaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('state', models.CharField(choices=[('PR', 'Prepare'), ('AP', 'Approved'), ('RJ', 'Recected'), ('CS', 'Concencus'), ('FN', 'Finish'), ('SP', 'Suspend')], default='PR', max_length=2)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('from_u', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='settletransaction_from_user', to=settings.AUTH_USER_MODEL)),
                ('settle', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bills.Settlement')),
                ('to_u', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='settletransaction_to_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=16)),
                ('state', models.CharField(choices=[('PR', 'Prepare'), ('AP', 'Approved'), ('RJ', 'Recected'), ('CS', 'Concencus'), ('FN', 'Finish'), ('SP', 'Suspend')], default='PR', max_length=2)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bills.Bill')),
                ('from_u', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transaction_from_user', to=settings.AUTH_USER_MODEL)),
                ('to_u', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='transaction_to_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bill',
            name='settlement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='Bills.Settlement'),
        ),
    ]
