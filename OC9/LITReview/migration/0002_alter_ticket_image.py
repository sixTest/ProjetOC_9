# Generated by Django 3.2.4 on 2021-07-13 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LITReview', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images'),
        ),
    ]
