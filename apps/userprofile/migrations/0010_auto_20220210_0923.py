# Generated by Django 3.0.7 on 2022-02-10 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userprofile', '0009_auto_20220209_1236'),
    ]

    operations = [
        migrations.AlterField(
            model_name='homeloan',
            name='aadhar',
            field=models.ImageField(upload_to=''),
        ),
    ]