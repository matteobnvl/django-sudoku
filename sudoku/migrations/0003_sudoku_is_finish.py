# Generated by Django 5.0 on 2023-12-19 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sudoku', '0002_player_groups_player_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='sudoku',
            name='is_finish',
            field=models.BooleanField(default=False),
        ),
    ]
