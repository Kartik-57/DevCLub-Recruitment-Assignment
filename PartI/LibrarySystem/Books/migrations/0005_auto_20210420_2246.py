# Generated by Django 3.2 on 2021-04-20 17:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_alter_availability_available'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Summary',
            new_name='Review',
        ),
        migrations.AlterField(
            model_name='book',
            name='Book_Cover',
            field=models.FileField(upload_to=''),
        ),
    ]
