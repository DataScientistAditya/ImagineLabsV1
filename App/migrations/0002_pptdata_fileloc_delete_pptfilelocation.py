# Generated by Django 4.0.4 on 2022-05-17 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='pptdata',
            name='FileLoc',
            field=models.FileField(default='N/a', upload_to='PptFiles'),
        ),
        migrations.DeleteModel(
            name='PptFileLocation',
        ),
    ]
