# Generated by Django 2.0 on 2019-02-26 18:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('travel_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Trip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('destination', models.CharField(max_length=255)),
                ('description', models.TextField(max_length=1000)),
                ('planned_by', models.CharField(max_length=255)),
                ('travel_date_from', models.DateField()),
                ('travel_date_to', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('users', models.ManyToManyField(related_name='trips', to='travel_app.User')),
            ],
        ),
    ]
