# Generated by Django 3.1.4 on 2020-12-22 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='slug',
            field=models.SlugField(default=None, max_length=30, unique=True),
            preserve_default=False,
        ),
    ]
