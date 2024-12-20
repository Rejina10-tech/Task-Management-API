from django.forms import ModelForm
from  .models import Task
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from django.forms.widgets import PasswordInput, TextInput
from django import forms
from . models import Task

class Taskform(ModelForm):
    
    class Meta:
        model = Task
        fields = '__all__'
        

class CreateUserForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']     

        
class LoginForm(AuthenticationForm):
      
      username = forms.CharField(widget=TextInput())
      password = forms.CharField(widget=PasswordInput())
      
    
class CreateTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields= ['Title', 'Description','Date','Completed']
        exclude= ['user',]

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class UpdateUserForm(forms.ModelForm):
    password = None

    class Meta:
        model = User
        fields = ['username', 'email']
        exclude = ['password1', 'password2']