# Generated by Django 4.1.1 on 2022-11-11 07:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home_page', '0002_message_updated_date_alter_message_accept_terms_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Message',
        ),
    ]