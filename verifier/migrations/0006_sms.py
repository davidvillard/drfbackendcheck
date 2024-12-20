# Generated by Django 5.1.3 on 2024-11-12 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('verifier', '0005_email_message_phone_message_url_message_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sms',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message_sms', models.CharField(max_length=100)),
                ('is_valid', models.BooleanField(default=False)),
                ('message', models.CharField(default='No message', max_length=100)),
                ('input_at', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
