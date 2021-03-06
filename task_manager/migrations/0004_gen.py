# Generated by Django 3.1.1 on 2020-09-29 19:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task_manager', '0003_auto_20200929_1956'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_of_fix', models.DateTimeField(blank=True)),
                ('description', models.TextField(null=True)),
                ('completion_time', models.DateTimeField(null=True)),
                ('title', models.CharField(blank=True, max_length=100, null=True)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history', to='task_manager.task')),
            ],
        ),
    ]
