# Generated by Django 4.1.5 on 2023-03-05 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_copybasedarticle_filebasedarticle'),
    ]

    operations = [
        migrations.DeleteModel(
            name='FileBasedArticle',
        ),
    ]
