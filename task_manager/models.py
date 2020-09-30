from django.db import models
from django.contrib.auth.models import User


class Task(models.Model):
    class TaskStatus(models.TextChoices):
        NEW = 'new'
        PLANNED = 'planned'
        IN_WORK = 'in work'
        COMPLETED = 'completed'

    title = models.CharField(default='Without title', blank=True, null=True, max_length=255)
    description = models.TextField(default='Without description', blank=True)
    creation_time = models.DateTimeField(blank=True, null=False)
    status = models.CharField(choices=TaskStatus.choices, blank=True, default=TaskStatus.NEW, max_length=20)
    completion_time = models.DateTimeField(null=True, blank=True)

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tasks', blank=True)

    def __str__(self):
        return self.title


class Gen(models.Model):

    time_of_fix = models.DateTimeField(blank=True)
    task = models.ForeignKey(Task, related_name='history', on_delete=models.CASCADE)

    description = models.TextField(null=True, blank=True)
    status = models.CharField(choices=Task.TaskStatus.choices, null=True, blank=True, max_length=20)
    completion_time = models.DateTimeField(null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)



