# Generated by Django 4.2.7 on 2024-01-30 17:34

from django.db import migrations, models
import django.db.models.deletion
import smartfarm.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(max_length=200, null=True)),
                ('file_title', models.CharField(max_length=200)),
                ('file_root', models.FileField(null=True, upload_to=smartfarm.models.user_file_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='FileStatusCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='LearnedModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=200)),
                ('model_meta_root', models.FileField(max_length=200, upload_to=smartfarm.models.user_model_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='smartfarm.file')),
            ],
        ),
        migrations.CreateModel(
            name='Temp',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_type', models.CharField(max_length=200, null=True)),
                ('file_title', models.CharField(max_length=200)),
                ('file_root', models.FileField(null=True, upload_to=smartfarm.models.user_temp_path)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('file', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='smartfarm.file')),
            ],
        ),
        migrations.CreateModel(
            name='TempStatusCode',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='TempStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartfarm.tempstatuscode')),
                ('temp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartfarm.temp')),
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
                ('temp', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='smartfarm.temp')),
            ],
        ),
        migrations.AddField(
            model_name='temp',
            name='statuses',
            field=models.ManyToManyField(through='smartfarm.TempStatus', to='smartfarm.tempstatuscode'),
        ),
        migrations.CreateModel(
            name='ModelFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_order', models.IntegerField()),
                ('feature_name', models.CharField(max_length=200)),
                ('weight', models.FloatField(null=True)),
                ('model', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='smartfarm.learnedmodel')),
            ],
        ),
        migrations.CreateModel(
            name='FileStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartfarm.file')),
                ('status', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='smartfarm.filestatuscode')),
            ],
        ),
        migrations.CreateModel(
            name='FileFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_order', models.IntegerField()),
                ('feature_name', models.CharField(max_length=200)),
                ('feature_type', models.CharField(max_length=200)),
                ('feature_importance', models.FloatField(null=True)),
                ('feature_selected', models.BooleanField(default=False)),
                ('file', models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='smartfarm.file')),
            ],
        ),
        migrations.AddField(
            model_name='file',
            name='statuses',
            field=models.ManyToManyField(through='smartfarm.FileStatus', to='smartfarm.filestatuscode'),
        ),
        migrations.AddField(
            model_name='file',
            name='user',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, to='users.user'),
        ),
    ]
