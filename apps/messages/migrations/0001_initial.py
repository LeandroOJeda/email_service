# Generated by Django 4.0.4 on 2023-10-23 00:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='message',
            fields=[
                ('id', models.AutoField(db_column='mensaje_id', primary_key=True, serialize=False)),
                ('subject', models.CharField(blank=True, db_column='mensaje_asunto', max_length=200)),
                ('body', models.TextField(blank=True, db_column='mensaje_texto', null=True)),
                ('from_email', models.CharField(db_column='mensaje_remitente', max_length=100)),
                ('to_email', models.CharField(db_column='mensaje_destinatario', max_length=100)),
                ('person', models.ForeignKey(db_column='mensaje_persona', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'mensajes',
            },
        ),
    ]