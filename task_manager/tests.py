from django.test import TestCase, Client
from task_manager.urls import urlpatterns
from django.urls import reverse
from task_manager import strings
from task_manager.models import User, Task
from datetime import datetime, timedelta
from rest_framework.authtoken.models import Token
import json


class TasksTestCase(TestCase):
    DEFAULT_USER = 'DefaultUser0'
    DEFAULT_PASSWORD = 'DefaultPassword0'

    @classmethod
    def setUpTestData(cls):
        user = User(username=cls.DEFAULT_USER)
        user.set_password(cls.DEFAULT_PASSWORD)
        user.save()
        Token.objects.create(user=user)
        task1 = Task(
            title='TestTask1',
            creation_time=datetime.now(),
            status=Task.TaskStatus.NEW,
            completion_time=(datetime.now() + timedelta(days=1)),
            creator=user
        )
        task2 = Task(
            title='TestTask2',
            creation_time=datetime.now(),
            status=Task.TaskStatus.COMPLETED,
            completion_time=(datetime.now() + timedelta(days=2)),
            creator=user
        )

        task3 = Task(
            title='TestTask3',
            creation_time=datetime.now(),
            status=Task.TaskStatus.NEW,
            completion_time=(datetime.now() + timedelta(days=3)),
            creator=user
        )

        user1 = User(username=cls.DEFAULT_USER.replace('0', '1'))
        user1.set_password(cls.DEFAULT_PASSWORD)
        user1.save()

        task4 = Task(
            title='TestTask4',
            creation_time=datetime.now(),
            status=Task.TaskStatus.NEW,
            completion_time=(datetime.now() + timedelta(days=3)),
            creator=user1
        )

        task1.save()
        task2.save()
        task3.save()
        task4.save()

    def test_sing_up_in(self):
        c = Client()
        name = 'TestUser1'

        response = c.post(path=reverse('user_create'), data={
            strings.PARAM_USER_NAME: name,
            strings.PARAM_USER_PASSWORD: 'TestPassword11'
        })

        self.assertEqual(response.data[strings.PARAM_USER_NAME], name, 'Not completed register')

        response = c.post(path=reverse('user_login'), data={
            strings.PARAM_USER_NAME: name,
            strings.PARAM_USER_PASSWORD: 'TestPassword11'
        })

        self.assertIn('token', response.data, 'Without token')

        response = c.post(path=reverse('user_login'), data={
            strings.PARAM_USER_NAME: name,
            strings.PARAM_USER_PASSWORD: ''
        })

        self.assertEqual(strings.USER_NOT_AUTH, response.data[strings.BAD_MESSAGE])

    def test_get_all_not_auth(self):
        c = Client()
        response = c.get(reverse('all_tasks'))
        self.assertEqual(response.data["detail"], "Authentication credentials were not provided.")

    def test_get_someones_task(self):
        c = Client()
        response = c.post(path=reverse('user_login'), data={
            strings.PARAM_USER_NAME: self.DEFAULT_USER,
            strings.PARAM_USER_PASSWORD: self.DEFAULT_PASSWORD
        })

        c = Client(HTTP_AUTHORIZATION='token {0}'.format(response.data['token']))
        response = c.get(reverse('one_task', args=[4]))
        self.assertEqual(response.data[strings.BAD_MESSAGE], strings.USER_NOT_AUTH)

    def test_get_my_task(self):
        c = Client()
        response = c.post(path=reverse('user_login'), data={
            strings.PARAM_USER_NAME: self.DEFAULT_USER,
            strings.PARAM_USER_PASSWORD: self.DEFAULT_PASSWORD
        })
        c = Client(HTTP_AUTHORIZATION='token {0}'.format(response.data['token']))
        response = c.get(reverse('all_tasks'))

        self.assertEqual(len(response.data), 3)

    def test_filter_my_task(self):
        c = Client()

        response = c.post(path=reverse('user_login'), data={
            strings.PARAM_USER_NAME: self.DEFAULT_USER,
            strings.PARAM_USER_PASSWORD: self.DEFAULT_PASSWORD
        })

        c = Client(HTTP_AUTHORIZATION='token {0}'.format(response.data['token']))
        response = c.get(reverse('all_tasks'),
                         {strings.PARAM_COND_BEFORE: (datetime.now() + timedelta(days=2)).
                         strftime(strings.DATETIME_TEMPLATE)})

        self.assertEqual(len(response.data), 2)

        response = c.get(reverse('all_tasks'),
                         {strings.PARAM_COND_BEFORE: (datetime.now() + timedelta(days=2)).
                         strftime(strings.DATETIME_TEMPLATE),
                          strings.PARAM_COND_AFTER: datetime.now().strftime(strings.DATETIME_TEMPLATE)})

        self.assertEqual(len(response.data), 2)

        response = c.get(reverse('all_tasks'),
                         {strings.PARAM_COND_BEFORE: (datetime.now() + timedelta(days=2)).
                         strftime(strings.DATETIME_TEMPLATE),
                          strings.PARAM_COND_AFTER: datetime.now().strftime(strings.DATETIME_TEMPLATE),
                          strings.PARAM_COND_STATUS: Task.TaskStatus.COMPLETED})

        self.assertEqual(len(response.data), 1)

    def test_one_task(self):
        c = Client()

        response = c.post(path=reverse('user_login'), data={
            strings.PARAM_USER_NAME: self.DEFAULT_USER,
            strings.PARAM_USER_PASSWORD: self.DEFAULT_PASSWORD
        })

        c = Client(HTTP_AUTHORIZATION='token {0}'.format(response.data['token']))
        response = c.get(reverse('one_task', args=[3]))

        self.assertEqual(response.status_code, 200)

    def test_edit_one_task(self):
        c = Client()
        response = c.post(path=reverse('user_login'), data={
            strings.PARAM_USER_NAME: self.DEFAULT_USER,
            strings.PARAM_USER_PASSWORD: self.DEFAULT_PASSWORD
        })

        c = Client(HTTP_AUTHORIZATION='token {0}'.format(response.data['token']))

        c.put(reverse('one_task', args=[2]), data='{"description": "new desc"}', content_type='application/json')
        response = c.get(reverse('one_task', args=[2]))
        self.assertEqual(response.data['description'], 'new desc')
        c.put(reverse('one_task', args=[2]), data='{"title": "new title"}', content_type='application/json')
        response = c.get('{0}{1}'.format(reverse('one_task', args=[2]), '?with_history=True'))

        self.assertEqual(len(response.data['task']['history']), 2)
        self.assertEqual(response.data['task']['history'][1]['description'], 'new desc')
