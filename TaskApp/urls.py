
from django.urls import path,include
from .views import *
from . import views
from .views import TaskDetailView,TaskListCreateView
from .views import TaskViewSet, LoginView
from rest_framework.routers import DefaultRouter
from .views import TaskList,TaskDetail # Assuming you have a TaskDetail view


router = DefaultRouter()
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = [
    path('api/', views.api_root, name='api_root'),
    path('api/tasks/', TaskList.as_view(), name='task-list-create'),
    path('api/tasks/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('tasks/', TaskCreateView.as_view(), name='task-create'),
    path('<int:pk>/', DetailTask.as_view()),
    # path('', ListTask.as_view()),

    
    path('', views.home, name=""),
    
    
    
    # delete task
    path('delete-task/<str:pk>', views.deleteTask, name='delete-task'),
    
    
    
    
    # read tasks
    path('view-task', views.viewTask, name="view-task"),
    
 
    
    # Create task
    
    path('create-task', views.createTask, name= "create-task"),
    
    
    
    
    # update task
    
    path('update-task/<str:pk>', views.updateTask, name= "update-task"),
    
    
    

    # register a user
    
    path("register", views.register, name="register" ),
    

    
  # login a user
    path('my-login', views.my_login, name="my-login" ),

    #logout a user
    
    path('user-logout', views.user_logout, name="user-logout" ),

    
    # dashboard
    path('dashboard', views.dashboard, name="dashboard" ),
    path('api/tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    
    # path('api/login/', api_login_user, name='api_login_user'),  # Login


    # path('api/tasks/', views.TaskListView.as_view(), name='task_list_create'),
    path('api/tasks/<int:pk>/', views.TaskDetailView.as_view(), name='task_detail'),
    path('api/register/', views.CreateUserView.as_view(), name='user_register'),
    path('api/login/', views.LoginView.as_view(), name='user_login'),

    path('api/login/', LoginView.as_view(), name='user_login'),

    path('tasks/', TaskViewSet.as_view({'get': 'list', 'post': 'create'}), name='task-list'),
    path('tasks/<int:pk>/', TaskViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='task-detail'),
]

