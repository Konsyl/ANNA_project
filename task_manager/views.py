from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from task_manager.serialisers import UserSerializer, TaskSerializer, GenSerializer
from rest_framework.response import Response
from django.contrib.auth import authenticate
from datetime import datetime
from task_manager.models import Task
from task_manager import strings


class InWork(APIView):
    permission_classes = ()

    def get(self, request):
        return HttpResponse(strings.SERVICE_WORKS)


class TasksController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        c_before = request.GET.get(strings.PARAM_COND_BEFORE)
        c_after = request.GET.get(strings.PARAM_COND_AFTER)
        status = request.GET.get(strings.PARAM_COND_STATUS)
        user = request.user

        if c_after or c_before or status:

            tasks = user.tasks

            if c_after and c_before:

                c_after = datetime.strptime(c_after, strings.DATETIME_TEMPLATE)
                c_before = datetime.strptime(c_before, strings.DATETIME_TEMPLATE)

                if c_after > c_before:
                    return Response({strings.BAD_MESSAGE: strings.INVALID_CONDITION}, status=401)

                tasks = tasks.filter(completion_time__range=[c_after, c_before])
            else:
                if c_after:
                    c_after = datetime.strptime(c_after, strings.DATETIME_TEMPLATE)
                    tasks = tasks.filter(completion_time__gte=c_after)

                if c_before:
                    c_before = datetime.strptime(c_before, strings.DATETIME_TEMPLATE)
                    tasks = tasks.filter(completion_time__lte=c_before)
            if status:
                if status in Task.TaskStatus:
                    tasks = tasks.filter(status=status)
                else:
                    try:
                        status = status.split(',')
                        if (set(status) & set(Task.TaskStatus.values)) == set(status):
                            tasks = tasks.filter(status__in=status)
                        else:
                            return Response({strings.BAD_MESSAGE: strings.INVALID_CONDITION})
                    except:
                        return Response({strings.BAD_MESSAGE: strings.INVALID_CONDITION})
        else:
            tasks = user.tasks.all()

        serializer = TaskSerializer(tasks,  many=True)
        return Response(serializer.data)

    def post(self, request):
        if request.GET.get(strings.PARAM_MANY_DATA_ALLOW) is True:
            serializer = TaskSerializer(data=request.data, many=True, context={'request': request})
        else:
            serializer = TaskSerializer(data=request.data, many=False, context={'request': request})
        if serializer.is_valid():
            serializer.create(validated_data=serializer.validated_data)
            return Response(strings.COMPLETE_MESSAGE, status=200)
        else:
            return Response({strings.BAD_MESSAGE: serializer.errors})


class TaskController(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        task = get_object_or_404(Task.objects.all(), pk=pk)
        if task.creator.pk is not request.user.pk:
            return Response({strings.BAD_MESSAGE: strings.USER_NOT_AUTH})
        serializer = TaskSerializer(task)
        if request.GET.get(strings.PARAM_OUT_WITH_HISTORY) == 'True':
            history = task.history

            history_serializer = GenSerializer(history, many=True)
            return Response({'task': {'data': serializer.data, 'history': history_serializer.data}})
        else:
            return Response(serializer.data)

    def put(self, request, pk):
        task = get_object_or_404(Task.objects.all(), pk=pk)
        serializer = TaskSerializer(data=request.data)

        if task.creator.pk is not request.user.pk:
            return Response({strings.BAD_MESSAGE: strings.USER_NOT_AUTH})

        if serializer.is_valid():
            if serializer.update(instance=task, validated_date=serializer.validated_data):

                return Response(strings.COMPLETE_MESSAGE, status=200)
            else:
                return Response(strings.BAD_MESSAGE, status=400)
        else:
            return Response({strings.BAD_MESSAGE: serializer.errors})

    def delete(self, request, pk):
        task = get_object_or_404(Task.objects.all(), pk=pk)
        if task.creator.pk is not request.user.pk:
            return Response({strings.BAD_MESSAGE: strings.USER_NOT_AUTH})

        task.delete()
        return Response(strings.COMPLETE_MESSAGE, status=200)


class UserCreate(APIView):
    authenticate_classes = ()
    permission_classes = ()

    def post(self, request):
        serializer = UserSerializer(data=request.data, many=False)

        if serializer.is_valid():
            new_user = serializer.create(validated_data=serializer.validated_data)
            if new_user:
                return Response(UserSerializer(new_user, many=False).data, status=201)
            else:
                return HttpResponse(strings.BAD_MESSAGE, status=400)
        else:
            return HttpResponse(strings.BAD_MESSAGE, status=400)


class LoginView(APIView):
    permission_classes = ()

    def post(self, request):
        username = request.data.get(strings.PARAM_USER_NAME)
        password = request.data.get(strings.PARAM_USER_PASSWORD)
        user = authenticate(username=username, password=password)
        if user:
            return Response({'token': user.auth_token.key})
        else:
            return Response({strings.BAD_MESSAGE: strings.USER_NOT_AUTH}, status=400)
