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
from django.http import Http404
from .serializers import TaskSerializer




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

    return render(request, 'read-task.html', context=context)

def home(request):
    
    # queryAllData = Task.objects.all()
    # querySingleObject = Task.objects.get(id=5)
    
    # context = {'tasks': queryAllData}
    return render(request, 'index.html')


# register a user
def register(request):
    
    form = CreateUserForm()
    if request.method == "POST":
        
        form = CreateUserForm(request.POST)
        
        if form.is_valid():
            
            form.save()
            
            return redirect('dashboard')
        
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
    
    
                
    
    
    
    
    # return render(request, "my-login.html")
    
    
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
          
        return redirect('read-task')
    
    context = {'form': form}
    
    return render(request, "profiles/create-task.html", context=context)


# view all tasks page

@login_required(login_url='my-login')
def readTask(request):
    
    current_user = request.user.id 
    task = Task.objects.all().filter(user=current_user)
    
    context = {'task': task}
    return render(request, 'profiles/read-task.html', context=context)

# update all tasks page

@login_required(login_url='my-login')
def updateTask(request, pk):
    
    task = Task.objects.get(id=pk)
    
    form = CreateTaskForm(instance=task)
    
    if request.method == 'POST':
        form = CreateTaskForm(request.POST, instance=task)
         
        if form.is_valid():
        
         
           form.save()
          
        return redirect('read-task')
    

    context = {'form': form}
    return render(request, 'profiles/update-task.html', context=context)

   
   
   
   
#    delete task
@login_required(login_url='my-login')
def deleteTask(request, pk):
    
    task = Task.objects.get(id=pk)
    
     
    if request.method == 'POST':
        
           task.delete()
          
           return redirect('read-task')
    

    return render(request, 'profiles/delete-task.html')

   
   
   
   
   
    
# logout a user

def user_logout(request):
    
    auth.logout(request)

    return redirect('my-login')



@login_required(login_url='my-login')
def dashboard(request):
    
    return render(request, 'profiles/dashboard.html')


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


# class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Task.objects.all()
#     serializer_class = TaskSerializer

#     def get_object(self, pk):
#         try:
#             return Task.objects.get(pk=pk)
#         except Task.DoesNotExist:
#             raise Http404
    


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
    })