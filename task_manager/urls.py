from django.urls import path
from task_manager.views import UserCreate, LoginView, InWork, TasksController, TaskController


urlpatterns = [
    path('inwork/', InWork.as_view(), name='check_work'),
    path('user/', UserCreate.as_view(), name='user_create'),
    path('login/', LoginView.as_view(), name='user_login'),
    path('mytasks/', TasksController.as_view(), name='all_tasks'),
    path('mytask/<int:pk>/', TaskController.as_view(), name='one_task')
]
