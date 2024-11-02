
from django.urls import path
from .views import *
from . import views
from .views import TaskDetailView, TaskListView
from .views import TaskListView


urlpatterns = [
    path('api/', views.api_root, name='api_root'),


    path('<int:pk>/', DetailTask.as_view()),
    # path('', ListTask.as_view()),
    
    path('', views.home, name=""),
    
    
    
    # delete task
    path('delete-task/<str:pk>', views.deleteTask, name='delete-task'),
    
    
    
    
    # read tasks
    path('read-task', views.readTask, name="read-task"),
    
    path('', views.home, name=""),
    
    
    # Create task
    
    path('create-task', views.createTask, name= "create-task"),
    
    
    
    
    # update task
    
    path('update-task/<str:pk>', views.updateTask, name= "update-task"),
    
    
    
    # path("read-task", views.readTask, name="read-task" ),
    
    
    # register a user
    
    path("register", views.register, name="register" ),
    
    
    
  # login a user
    path('my-login', views.my_login, name="my-login" ),

    #logout a user
    
    path('user-logout', views.user_logout, name="user-logout" ),

    
    # dashboard
    path('dashboard', views.dashboard, name="dashboard" ),


    path('api/tasks/', views.TaskListView.as_view(), name='task_list_create'),
    path('api/tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('api/register/', views.CreateUserView.as_view(), name='user_register'),
]