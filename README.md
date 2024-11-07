
# Task Management API

This is a RESTful API for a Task Management system, built using Django and Django REST Framework (DRF). 
The API allows users to create, update, delete, and retrieve tasks.



## Features
- CRUD Operations: Create, read, update, and delete tasks.

- User Authentication: Manage user authentication and authorization for secure access.

## Prerequisites
Python

PostgreSQL 

Django and Django REST Framework

## Installation

Clone the Repository

```bash
  git clone https://github.com/Rejina10-tech/Task-Management-API.git
```

Set Up a Virtual Environment

```bash
source taskenv/Scripts/activate 
```
        or
```bash
source newenv/Scripts/activate 
```

Install Dependencies
```bash
  Django

  Django REST Framework 
  
  PostgreSQL 
```
Install Requirements
```bash
  pip install -r requirements.txt
```

Configure the Database
```bash
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

```
Run Migrations
```bash
  python manage.py migrate
  ```

Start the Server
```bash
  python manage.py runserver
  ```
  



    
## API Endpoints

#### Create a new task

```http
  POST /api/tasks
```



#### Retrieve all tasks

```http
  GET /api/tasks
```

#### Retrieve a specific task
```http
  GET /api/tasks/{id}
```

#### Update a specific task
```http
  PUT /api/tasks/{id}
```

#### Delete a specific task
```http
  DELETE /api/tasks/{id}
```






## Technologies Used

 - Django
 - Django RestFramework
 - Postgresql

