# Generated by Django 4.2.7 on 2024-05-01 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FileFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_order', models.IntegerField()),
                ('feature_name', models.CharField(max_length=200)),
                ('feature_type', models.CharField(max_length=200)),
                ('feature_importance', models.FloatField(null=True)),
                ('feature_selected', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='ModelFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_name', models.CharField(max_length=200)),
                ('weight', models.FloatField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TempFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_order', models.IntegerField()),
                ('feature_name', models.CharField(max_length=200)),
                ('feature_type', models.CharField(max_length=200)),
                ('feature_importance', models.FloatField(null=True)),
                ('feature_selected', models.BooleanField(default=False)),
            ],
        ),
    ]
