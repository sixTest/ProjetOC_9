# Generated by Django 3.2.4 on 2021-07-13 13:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LITReview', '0004_alter_ticket_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
    ]
