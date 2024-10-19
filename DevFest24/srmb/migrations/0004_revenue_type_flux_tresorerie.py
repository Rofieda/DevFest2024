# Generated by Django 5.0.2 on 2024-10-18 17:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('srmb', '0003_recommendation'),
    ]

    operations = [
        migrations.AddField(
            model_name='revenue',
            name='type_flux_tresorerie',
            field=models.CharField(choices=[('opérationnelle', 'Opérationnelle'), ('investissement', 'Investissement'), ('financement', 'Financement')], default='opérationnelle', max_length=50),
            preserve_default=False,
        ),
    ]
