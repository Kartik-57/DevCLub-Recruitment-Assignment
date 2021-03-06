# Generated by Django 3.2 on 2021-04-17 14:03

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Author', models.CharField(max_length=100)),
                ('Publisher', models.CharField(max_length=200)),
                ('Book_Title', models.CharField(max_length=200)),
                ('Genre', models.CharField(max_length=100)),
                ('Book_Cover', models.CharField(max_length=1000)),
                ('ISBN', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Summary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
            ],
        ),
    ]
