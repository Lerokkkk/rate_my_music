# Generated by Django 4.2.10 on 2024-03-11 13:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_composition_featured_artist_alter_composition_artist'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='collaborative_artist',
            field=models.ManyToManyField(blank=True, related_name='collaborative_artist', to='main.artist'),
        ),
        migrations.AlterField(
            model_name='composition',
            name='composition_type',
            field=models.CharField(choices=[('SOLO', 'Solo'), ('FEAT', 'Feature'), ('COLLAB', 'Collaborative'), ('COLLAB_FEAT', 'Collaborative Feature')], default='SOLO', max_length=11),
        ),
    ]
