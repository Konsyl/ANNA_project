# Generated by Django 3.1.1 on 2020-09-29 14:18

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
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='Without title', max_length=255, null=True)),
                ('description', models.TextField(blank=True, default='Without description')),
                ('creation_time', models.DateTimeField(blank=True)),
                ('status', models.CharField(choices=[('new', 'New'), ('planned', 'Planned'), ('in work', 'In Work'), ('completed', 'Completed')], max_length=20)),
                ('completion_date', models.DateTimeField(blank=True, null=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]