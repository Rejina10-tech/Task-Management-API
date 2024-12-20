from django.shortcuts import render,redirect
from rest_framework import generics,  permissions
from .serializers import *
from .serializers import TaskSerializer
from django.contrib.auth.decorators import login_required
from .serializers import TaskSerializer, UserSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Task
from django.http import HttpResponse
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate,login
from .forms  import Taskform,CreateUserForm,LoginForm,CreateTaskForm
from .forms  import UpdateUserForm,Taskform, LoginForm, CreateUserForm
from django.contrib.messages import constants as message_constants

from .serializers import TaskSerializer
from rest_framework import viewsets
from .serializers import TaskSerializer 
from rest_framework.permissions import AllowAny  # Allow unauthenticated access
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer, LoginSerializer
from rest_framework import status
from .forms import UserRegistrationForm
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib import messages
from rest_framework.generics import UpdateAPIView
from django.contrib import messages



class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        if task.user != request.user:
            return Response({'detail': 'Not permitted to access this task.'}, status=status.HTTP_403_FORBIDDEN)
        return super().get(request, *args, **kwargs)
        
class TaskDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = super().get_object()
        if obj.user != self.request.user:
            raise PermissionDenied("You do not have permission to access this task.")
        return obj

class TaskUpdateView(UpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'  # Use 'id' to look up the task in the URL

class TaskList(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)        

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)
    
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)
    

class ListTask(generics.ListAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
class DetailTask(generics.RetrieveUpdateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
class CreateTask(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
class DeleteTask(generics.DestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    
    
def ReadTask(request):

    task = Task.objects.all()

    context = {'task': task}

    return render(request, 'view-task.html', context=context)

def home(request):
    return render(request, 'index.html')


# register a user
def register(request):
    
    form = CreateUserForm()
    if request.method == "POST":
        
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            
            form.save()

            messages.success(request, "User registration was successful !!" )
            
            return redirect('my-login')
        
    context = {'form':form}
    
    return render (request, "register.html", context=context)


# login a user

def my_login(request):
    
    form = LoginForm
    if request.method == 'POST':
        form = LoginForm(request, data = request.POST)
        
        if form.is_valid():
            
            username= request.POST.get("username")
            password = request.POST.get("password")
            
            user = authenticate(request, username=username, password= password)
            
            if user is not None:
                
                auth.login(request, user)
                return redirect("dashboard")
            
    context ={'form':form}
    
    return render(request, 'my-login.html', context=context)
    
    
    
# create  a task page
@login_required(login_url='my-login')
def createTask(request):
    
    form = CreateTaskForm()
    
    if request.method == 'POST':
        form = CreateTaskForm(request.POST)
         
        if form.is_valid():
         
         task = form.save(commit=False)
         
         task.user = request.user
         form.save()
          
        return redirect('view-task')
    
    context = {'form': form}
    
    return render(request, "profiles/create-task.html", context=context)


# view all tasks page

@login_required(login_url='my-login')
def viewTask(request):
    
    current_user = request.user.id 
    task = Task.objects.all().filter(user=current_user)
    
    context = {'task': task}
    return render(request, 'profiles/view-task.html', context=context)

# update all tasks page

@login_required(login_url='my-login')
def updateTask(request, pk):
    
    task = Task.objects.get(id=pk)
    
    form = CreateTaskForm(instance=task)
    
    if request.method == 'POST':
        form = CreateTaskForm(request.POST, instance=task)
         
        if form.is_valid():
        
         
           form.save()
          
        return redirect('view-task')
    

    context = {'form': form}
    return render(request, 'profiles/update-task.html', context=context)

   
   
   
   
#    delete task
@login_required(login_url='my-login')
def deleteTask(request, pk):
    
    task = Task.objects.get(id=pk)
    
     
    if request.method == 'POST':
        
           task.delete()
          
           return redirect('view-task')
    

    return render(request, 'profiles/delete-task.html')

   
   
   
   
    
# logout a user

def user_logout(request):
    
    auth.logout(request)

    return redirect('my-login')



@login_required(login_url='my-login')
def dashboard(request):
    
    return render(request, 'profiles/dashboard.html')


@login_required(login_url='my-login')
def profile_management(request):
    if request.method == 'POST':

      user_form = UpdateUserForm(request.POST, instance= request.user)

      if user_form.is_valid():
          
          user_form.save()

          return redirect ('dashboard')

    user_form = UpdateUserForm(instance=request.user)
    context = {'user_form': user_form}

    return render(request, 'profiles/profile-management.html', context=context)


@login_required(login_url='my-login')
def deleteAccount(request):
    if request.method == 'POST':
        deleteUser = User.objects.get(username=request.user)

        deleteUser.delete()

        return redirect('')
    
    return render(request, 'profiles/delete-account.html')







# Task API views
class TaskListView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        #filter tasks by logged user
        return  Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Set the user as the logged-in user when creating a task
        serializer.save(user=self.request.user)

    

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        #ensure only tasks owned by user can be accesed
        return  Task.objects.filter(user=self.request.user)


# User registration API view
class CreateUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]




# API Root View
@api_view(['GET'])
def api_root(request, format=None):
    return Response({
        'tasks': request.build_absolute_uri('/api/tasks/'),
        'register': request.build_absolute_uri('/api/register/'),
        'login': request.build_absolute_uri('/api/login/'),

    })


# View to list all tasks or create a new task
class TaskListCreateView(generics.ListCreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

# View to retrieve, update, or delete a specific task
class TaskRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        
        # Optionally return a token or other user information
        return Response({
            "message": "Login successful",
            "username": user.username,
            "email": user.email,
        }, status=status.HTTP_200_OK)



@api_view(['POST'])
def register_user(request):
    print("Received request data:", request.data)  
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # Save the user instance
        response_data = {
            'username': user.username,
            'email': user.email,
           
        }
        print("User registered successfully:", response_data)   
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        print("Validation errors:", serializer.errors)  
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

