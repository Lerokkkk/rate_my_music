# Generated by Django 4.2.10 on 2024-03-19 12:08

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_alter_artist_options_alter_composition_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='composition',
            name='artists_slug',
        ),
    ]