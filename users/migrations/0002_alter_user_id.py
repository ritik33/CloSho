# Generated by Django 3.2.3 on 2021-05-28 14:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='id',
            field=models.UUIDField(default='2dfc8162ea1a476aa37ae0ffc431df25', primary_key=True, serialize=False, unique=True),
        ),
    ]
