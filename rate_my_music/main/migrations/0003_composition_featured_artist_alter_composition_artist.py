# Generated by Django 4.2.10 on 2024-03-11 13:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_composition_delete_album'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='featured_artist',
            field=models.ManyToManyField(blank=True, related_name='featured_artist', to='main.artist'),
        ),
        migrations.AlterField(
            model_name='composition',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='artist', to='main.artist'),
        ),
    ]