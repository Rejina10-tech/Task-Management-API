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
from rest_framework import viewsets
from .serializers import TaskSerializer 
from rest_framework.permissions import AllowAny  # Allow unauthenticated access
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from .serializers import UserSerializer 
from rest_framework import status
from .forms import UserRegistrationForm




class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]  


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

# @api_view(['POST'])
# def register_user(request):
#     if request.method == 'POST':
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             # Hash the password before saving
#             serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def register_user(request):
    print("Received request data:", request.data)  # Debugging output
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()  # Save the user instance
        response_data = {
            'username': user.username,
            'email': user.email,
            # Add other fields you want to expose here if necessary
        }
        print("User registered successfully:", response_data)  # Debugging output
        return Response(response_data, status=status.HTTP_201_CREATED)
    else:
        print("Validation errors:", serializer.errors)  # Debugging output
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def api_register_user(request):
    form = UserRegistrationForm(data=request.data)
    if form.is_valid():
        user = form.save()
        login(request, user)  # Optionally log in the user
        return Response({"message": "User registered successfully!"}, status=201)
    return Response(form.errors, status=400)


@api_view(['POST'])
def api_login_user(request):
    serializer = UserLoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(username=serializer.validated_data['username'], password=serializer.validated_data['password'])
        if user is not None:
            login(request, user)  # Log the user in (optional)
            return Response({"message": "User logged in successfully!"}, status=status.HTTP_200_OK)
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
