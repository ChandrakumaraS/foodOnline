# Generated by Django 5.0.6 on 2024-08-14 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0003_tax'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='tax',
            options={'verbose_name_plural': 'tax'},
        ),
        migrations.RenameField(
            model_name='tax',
            old_name='is_activa',
            new_name='is_active',
        ),
    ]
