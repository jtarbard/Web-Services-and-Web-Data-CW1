# Generated by Django 4.0.3 on 2022-03-25 12:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rmp', '0002_alter_customuser_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='email',
            field=models.EmailField(blank=True, max_length=254, verbose_name='email address'),
        ),
    ]
