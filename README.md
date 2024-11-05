# Task Management API
This is a RESTful API for a Task Management system, built using Django and Django REST Framework (DRF). 
The API allows users to create, update, delete, and retrieve tasks, along with managing task status, deadlines, and priorities.

# Features
CRUD Operations: Create, read, update, and delete tasks.
User Authentication: Manage user authentication and authorization for secure access.

# Prerequisites
Python 
PostgreSQL 
Django and Django REST Framework

# Installation

1.Clone the Repository
  git clone https://github.com/Rejina10-tech/Portfolio-Website.git

2.Set Up a Virtual Environment
  source taskenv/bin/activate 

3.Install Dependencies
  Django - High-level Python web framework.
  Django REST Framework - Toolkit for building Web APIs.
  PostgreSQL - Relational database for storing tasks and user data.

4.Configure the Database
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'Task_Management',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': 'localhost', 
        'PORT': '5432', 
    }
}

5.Run Migrations
  python manage.py migrate


6.Start the Server
  python manage.py runserver

# API Endpoints
  /api/tasks/	: Create a new task
  /api/tasks/	: Retrieve all tasks
  /api/tasks/{id}/	: Retrieve a specific task
  /api/tasks/{id}/	: Update a specific task
  /api/tasks/{id}/	: Delete a specific task

# Technologies Used
  Django - High-level Python web framework.
  Django REST Framework - Toolkit for building Web APIs.
  PostgreSQL - Relational database for storing tasks and user data.
