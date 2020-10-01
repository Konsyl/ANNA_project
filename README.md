# REST API TASK MANAGER
Персонализированный менеджер задач.
Созданный для ANNA.money, сервис task manager, позволяющий пользователь. ставить себе задачи, отражать в системе изменение их статуса и просматривать историю изменения задач.

## Fast description
- Сервис разработан на python 3.7
- Хранение данных: PostgreeSQL
- Формат представления данных: JSON
- Авторизация: при помощи токена

## Functions of service
### Работа с пользователями
- Возможность регистрации пользователя по средствам предоставления пары:
POST request /tasks/user/:
```
{
	"username": "name",
	"password": "Password1234"
}
```
response:
```
{
	"username": "name",
}
```
- Возможность аутентификации
POST request /tasks/login/:
```
{
	"username": "username",
	"password": "Password1234"
}
```
response:
```
{
	"token": "9b7c9d04a1b45c6d25d7d39c6f4586b30d429fe9"
}
```
### Работа с задачами
#### Задача
- __Название задачи__
- __Описание__
- __Время создания__
- __Статус__
- __Планируемое время завершения__
- __Создатель__

#### Функции

- Возможность добавления задачи
POST request /tasks/mytasks/?many=True/False:
 - many=True - разрешение на добавление нескольких задач
 - many=False - запрет на добавление нескольких задач
```
        [{
        "title": " task1",
        "description": "1",
        "status": "new",
        "completion_time": "2020-12-30T14:26:48Z"
		},
		{
	    "title": " task2",
        "description": "2",
        "status": "new",
        "completion_time": "2020-12-30T14:28:48Z"
		}]
```
positive response:
```
{
"Completed"
}
```
negative response:
```
{
{'BAD REQUEST': ERRORS}
}
```
-  Возможность получить список задач (с фильтрацией по статусу и времени завершения)
GET request /tasks/mytasks:
__Параметры:__
 - complete_after - Завершена после указанной даты [%Y-%m-%dT%H:%M:%SZ]
 - complete_before - Завершена до указанной даты [%Y-%m-%dT%H:%M:%SZ]
  - status - Имеет следующий статус
  - При отсутствии параметров будут получены все задачи
__Возможно получить только свои задачи с условием авторизации__
Для авторизации: поместить __Authorization__ token 'токен' в заголовке запроса
Результат:
```
[
    {
        "id": 2,
        "title": "Test task2",
        "description": "2",
        "creation_time": "2020-09-30T08:47:17Z",
        "status": "new",
        "completion_time": "2020-12-30T14:28:48Z",
        "creator": 1
    },
    {
        "id": 1,
        "title": "Test task1",
        "description": "6 and 8",
        "creation_time": "2020-09-30T08:47:17Z",
        "status": "new",
        "completion_time": "2020-12-30T14:26:48Z",
        "creator": 1
    }
]
```
Результат без __Authorization__ в заголовке:
```
{
    "detail": "Authentication credentials were not provided."
}
```
#### Работа с конкретной задачей
- Возможность получения конкретной задачи (только своей)
GET request /tasks/mytask/__id__/
 параметры:
  - with_history=True/Flalse
  	True - задача будет получена с историй изменений
	False - задача будет получена без истории изменений
Результат:
```
"task": {
        "data": {
            "id": 1,
            "title": "Test task1",
            "description": "6 and 8",
            "creation_time": "2020-09-30T08:47:17Z",
            "status": "new",
            "completion_time": "2020-12-30T14:26:48Z",
            "creator": 1
        },
        "history": [
            {
                "id": 1,
                "description": "6 and 7"
            }
        ]
    }
}
```
Результат запроса чужой задачи:
```
{
"BAD REQUEST": "user not authenticate"
}
```
- Возможность изменять описание, время завершения и статус задачи
 PUT request /tasks/mytask/id/:
```
{
    "description": "new description"
}
```
Результат: "Completed"
Результат при неверных данных:

 ```
{'BAD REQUEST':  errors}
```
### Запуск
В каталоге с файлами проекта
```
docker-compose up -build 
```
### Проверка работы
GET request /tasks/inwork/
Результат:
	'Service works'
