# Generated by Django 4.1.4 on 2022-12-20 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pagos', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id_services', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=200)),
                ('logo', models.URLField()),
            ],
        ),
    ]
