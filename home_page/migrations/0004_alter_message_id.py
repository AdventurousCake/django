# Generated by Django 4.1 on 2022-08-21 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0003_message_author'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='id',
            field=models.IntegerField(auto_created=True, max_length=10, primary_key=True, serialize=False, unique=True),
        ),
    ]