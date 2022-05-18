# Generated by Django 4.0.4 on 2022-05-17 10:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PptData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Query', models.CharField(max_length=500)),
                ('isLayman', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='PptFileLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('FileLoc', models.FileField(upload_to='PptFiles')),
                ('Query', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='App.pptdata')),
            ],
        ),
    ]
