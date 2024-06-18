# Generated by Django 4.2 on 2024-05-29 12:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0011_alter_rate_rate'),
    ]

    operations = [
        migrations.AddField(
            model_name='composition',
            name='is_published',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='rate',
            name='rate',
            field=models.CharField(choices=[('1', '1'), ('2', '2'), ('3', '3'), ('4', '4'), ('5', '5'), ('6', '6'), ('7', '7'), ('8', '8'), ('9', '9'), ('10', '10')], max_length=2, verbose_name='Оценка'),
        ),
    ]
