from collections import OrderedDict
from rest_framework import serializers
from task_manager.models import Task, Gen
from datetime import datetime
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def create(self, validated_data):
        task = Task(title=validated_data['title'],
                    description=validated_data['description'],
                    creation_time=datetime.now(),
                    status=Task.TaskStatus.NEW,
                    completion_time=validated_data['completion_time'],
                    creator=self.context['request'].user
                    )

        task.save()
        return True

    def update(self, instance, validated_date):

        gen = Gen(task=instance, time_of_fix=datetime.now())

        if 'description' in validated_date:
            gen.description = validated_date['description']
            instance.description = validated_date['description']
        if 'completion_time' in validated_date:
            gen.completion_time = validated_date['completion_time']
            instance.completion_time = validated_date['completion_time']
        if 'title' in validated_date:
            gen.title = validated_date['title']
            instance.title = validated_date['title']
        if 'status' in validated_date:
            gen.status = validated_date['status']
            instance.status = validated_date['status']

        if any([gen.title, gen.description, gen.completion_time, gen.status]):
            gen.save()

        instance.save()

        return True


class GenSerializer(serializers.ModelSerializer):

    def to_representation(self, value):
        repr_dict = super(GenSerializer, self).to_representation(value)
        return OrderedDict((k, v) for k, v in repr_dict.items()
                           if v not in [None, [], '', {}])

    class Meta:
        model = Gen
        fields = ('id', 'title', 'description', 'status', 'completion_time',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(username=validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user
