

from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Task

class TaskAPITestCase(APITestCase):

    def setUp(self):
        # Create two users
        self.user1 = User.objects.create_user(username='user1', password='password1')
        self.user2 = User.objects.create_user(username='user2', password='password2')

        # Create tasks for both users
        self.task1 = Task.objects.create(
            Title='Task 1',
            Description='Description for Task 1',
            Date='2024-11-05',
            Completed=False,
            user=self.user1,
        )
        self.task2 = Task.objects.create(
            Title='Task 2',
            Description='Description for Task 2',
            Date='2024-11-06',
            Completed=False,
            user=self.user2,
        )

    def test_get_task_list(self):
        # Log in as user1
        self.client.login(username='user1', password='password1')

        # Retrieve task list
        response = self.client.get(reverse('task-list-create'))

        # Only user1's task should be visible
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['Title'], self.task1.Title)

    def test_get_single_task(self):
        # Log in as user1
        self.client.login(username='user1', password='password1')

        # Retrieve user1's task
        response = self.client.get(reverse('task-detail', args=[self.task1.pk]))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['Title'], self.task1.Title)

    def test_get_task_user_access(self):
        # Log in as user1
        self.client.login(username='user1', password='password1')

        # Attempt to retrieve user2's task
        response = self.client.get(reverse('task-detail', args=[self.task2.pk]))

        # Assert that user1 cannot access user2's task
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_task(self):
        # Log in as user1
        self.client.login(username='user1', password='password1')

        # Create a new task
        response = self.client.post(reverse('task-list-create'), {
            'Title': 'New Task',
            'Description': 'New task description',
            'Date': '2024-11-07',
            'Completed': False,
            'user': self.user1.pk,  # User must be assigned to the task
        })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 3)  # Ensure task count is updated
        self.assertEqual(Task.objects.last().Title, 'New Task')

    def test_update_task(self):
        # Log in as user1
        self.client.login(username='user1', password='password1')

        # Update task1
        response = self.client.put(reverse('task-detail', args=[self.task1.pk]), {
            'Title': 'Updated Task 1',
            'Description': 'Updated description',
            'Date': '2024-11-08',
            'Completed': True,
            'user': self.user1.pk,
        })

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()  # Refresh task from DB to get updated data
        self.assertEqual(self.task1.Title, 'Updated Task 1')

    def test_delete_task(self):
        # Log in as user1
        self.client.login(username='user1', password='password1')

        # Delete task1
        response = self.client.delete(reverse('task-detail', args=[self.task1.pk]))

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 1)  # Ensure one task is deleted


    def test_get_task_user_access(self):
    # User1 accesses User2's task
        self.client.force_authenticate(user=self.user1)  # Authenticate as user1
        response = self.client.get(reverse('task-detail', args=[self.task2.pk]))  # Assuming task2 belongs to user2
        # self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)  # Should return 403 for unauthorized access
