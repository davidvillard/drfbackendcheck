# Generated by Django 5.1.3 on 2024-11-22 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifier', '0009_remove_email_input_at_local_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=100)),
                ('email', models.CharField(max_length=100)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
    ]
