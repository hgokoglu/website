# Generated by Django 4.1.5 on 2023-05-11 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_article_news_caster_alter_article_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='news_caster',
            field=models.CharField(default='', max_length=64),
        ),
    ]
