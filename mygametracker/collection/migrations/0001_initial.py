# Generated by Django 5.0 on 2023-12-08 04:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('collection_id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
            ],
        ),
    ]
